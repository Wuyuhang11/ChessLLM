import torch
import torch.nn as nn
import torch.nn.functional as F

class BasicExpert(nn.Module):
    def __init__(self, feature_in, feature_out):
        super().__init__()
        self.fc = nn.Linear(feature_in, feature_out)
    
    def forward(self, x):
        return self.fc(x)

class BasicMOE(nn.Module):
    def __init__(self, feature_in, feature_out, num_experts):
        super().__init__()
        self.gate = nn.Linear(feature_in, num_experts)  # 修正了 super.gate 为 self.gate
        self.experts = nn.ModuleList(
            BasicExpert(feature_in, feature_out) for _ in range(num_experts)
        )
    
    def forward(self, x): 
        expert_weights = self.gate(x)
        expert_out_list = [
            expert(x) for expert in self.experts
        ]  # 每个expert输出一个(batch, feature_out)
        
        # expert_out:(b, 1, feature_out)
        expert_outputs = [
            expert_out.unsqueeze(1)
            for expert_out in expert_out_list
        ]
        
        expert_output = torch.concat(
            expert_outputs,
            dim=1,
        )  # expert_output:(b, num_experts, feature_out)
        
        # expert_weights:(b, num_experts)
        expert_weights = F.softmax(expert_weights, dim=1)
        
        expert_weights = expert_weights.unsqueeze(1)  # (b, 1, num_experts)
        output = expert_weights @ expert_output
        return output.squeeze(1)

# 将 test_basic_moe 定义为独立的函数
def test_basic_moe():
    x = torch.rand(4, 512)  # (b, feature_in)
    basic_moe = BasicMOE(512, 128, 4)  # (feature_in, feature_out, num_experts)
    output = basic_moe(x)
    print(output.shape)

# 调用测试函数
test_basic_moe()