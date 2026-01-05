#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球2026002期号码推算脚本
基于最近30期历史数据进行24码分析并生成投注方案
"""

import random
from collections import Counter
from typing import List, Tuple, Dict


class LotteryAnalyzer:
    """双色球号码分析器"""
    
    def __init__(self):
        self.history_data = []
        
    def load_history_data(self, data: List[Tuple[str, List[int], int]]):
        """
        加载历史数据
        data格式: [(期号, [红球1-6], 蓝球), ...]
        """
        self.history_data = data
        print(f"✅ 已加载 {len(data)} 期历史数据")
    
    def analyze_24_codes(self) -> List[int]:
        """分析生成24码主流区间"""
        if len(self.history_data) < 30:
            print(f"⚠️  警告：历史数据不足30期，当前仅有{len(self.history_data)}期")
        
        # 统计所有红球出现次数
        all_reds = []
        for period, reds, blue in self.history_data[-30:]:  # 取最近30期
            all_reds.extend(reds)
        
        # 计数并排序
        counter = Counter(all_reds)
        sorted_balls = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        
        # 取前24个
        codes_24 = [ball for ball, count in sorted_balls[:24]]
        
        print(f"\n📊 24码主流区间分析（基于最近{min(len(self.history_data), 30)}期）")
        print("=" * 60)
        print(f"{'号码':<8}{'出现次数':<12}{'出现频率'}")
        print("-" * 60)
        
        for i, (ball, count) in enumerate(sorted_balls[:24], 1):
            freq = count / min(len(self.history_data), 30)
            print(f"{ball:02d}      {count:<12}{freq:>6.1%}")
        
        print("=" * 60)
        print(f"24码列表: {', '.join([f'{x:02d}' for x in sorted(codes_24)])}")
        
        return sorted(codes_24)
    
    def validate_template_a(self, nums: List[int]) -> bool:
        """验证模板A：3奇3偶 + 3小3大 + 连号≤1 + 同尾≤1"""
        # 奇偶
        odd = sum(1 for n in nums if n % 2 == 1)
        even = 6 - odd
        if odd != 3 or even != 3:
            return False
        
        # 大小
        small = sum(1 for n in nums if n <= 16)
        large = 6 - small
        if small != 3 or large != 3:
            return False
        
        # 连号
        consecutive = sum(1 for i in range(5) if nums[i+1] - nums[i] == 1)
        if consecutive > 1:
            return False
        
        # 同尾
        same_tail = 0
        for i in range(5):
            for j in range(i+1, 6):
                if nums[i] % 10 == nums[j] % 10:
                    same_tail += 1
        if same_tail > 1:
            return False
        
        return True
    
    def validate_template_b(self, nums: List[int]) -> bool:
        """验证模板B：2奇4偶 + 2小4大 + 连号≤1 + 同尾≤2"""
        # 奇偶
        odd = sum(1 for n in nums if n % 2 == 1)
        even = 6 - odd
        if odd != 2 or even != 4:
            return False
        
        # 大小
        small = sum(1 for n in nums if n <= 16)
        large = 6 - small
        if small != 2 or large != 4:
            return False
        
        # 连号
        consecutive = sum(1 for i in range(5) if nums[i+1] - nums[i] == 1)
        if consecutive > 1:
            return False
        
        # 同尾
        same_tail = 0
        for i in range(5):
            for j in range(i+1, 6):
                if nums[i] % 10 == nums[j] % 10:
                    same_tail += 1
        if same_tail > 2:
            return False
        
        return True
    
    def generate_bet(self, codes_24: List[int], template: str = 'A') -> List[int]:
        """生成一注投注号码"""
        max_attempts = 1000
        
        for attempt in range(max_attempts):
            # 随机选择6个号码
            selected = random.sample(codes_24, 6)
            selected.sort()
            
            # 验证
            if template == 'A' and self.validate_template_a(selected):
                return selected
            elif template == 'B' and self.validate_template_b(selected):
                return selected
        
        # 如果1000次都没成功，使用简单策略
        print(f"⚠️  模板{template}难以满足，使用简化策略")
        selected = random.sample(codes_24, 6)
        selected.sort()
        return selected
    
    def generate_betting_scheme(self, period: str, codes_24: List[int], num_bets: int = 10) -> List[Dict]:
        """生成投注方案"""
        print(f"\n🎯 {period}期投注方案生成")
        print("=" * 70)
        
        scheme = []
        num_template_a = int(num_bets * 0.8)  # 80%
        num_template_b = num_bets - num_template_a  # 20%
        
        # 生成模板A方案
        for i in range(num_template_a):
            reds = self.generate_bet(codes_24, 'A')
            blue = random.randint(1, 16)
            scheme.append({
                'bet_num': i + 1,
                'template': 'A',
                'reds': reds,
                'blue': blue
            })
        
        # 生成模板B方案
        for i in range(num_template_b):
            reds = self.generate_bet(codes_24, 'B')
            blue = random.randint(1, 16)
            scheme.append({
                'bet_num': num_template_a + i + 1,
                'template': 'B',
                'reds': reds,
                'blue': blue
            })
        
        # 显示方案
        print(f"{'注号':<6}{'模板':<6}{'红球号码':<30}{'蓝球':<6}{'验证'}")
        print("-" * 70)
        
        for bet in scheme:
            reds_str = ' '.join([f"{x:02d}" for x in bet['reds']])
            
            # 分析特征
            odd = sum(1 for n in bet['reds'] if n % 2 == 1)
            small = sum(1 for n in bet['reds'] if n <= 16)
            
            features = f"{odd}奇{6-odd}偶·{small}小{6-small}大"
            
            print(f"{bet['bet_num']:<6}{bet['template']:<6}{reds_str:<30}{bet['blue']:02d}    {features}")
        
        print("=" * 70)
        print(f"✅ 共生成 {num_bets} 注投注方案（{num_template_a}注模板A + {num_template_b}注模板B）")
        
        return scheme
    
    def analyze_hot_cold_numbers(self) -> Tuple[List[int], List[int]]:
        """分析热号和冷号"""
        # 统计所有红球
        all_reds = []
        for period, reds, blue in self.history_data[-30:]:
            all_reds.extend(reds)
        
        counter = Counter(all_reds)
        
        # 热号（出现频率高）
        sorted_balls = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        hot_numbers = [ball for ball, count in sorted_balls[:10]]
        
        # 冷号（出现频率低）
        all_balls = set(range(1, 34))
        appeared_balls = set(counter.keys())
        cold_numbers = list(all_balls - appeared_balls)
        
        # 补充冷号（出现次数少的）
        if len(cold_numbers) < 10:
            for ball, count in sorted(counter.items(), key=lambda x: x[1])[:10]:
                if ball not in cold_numbers:
                    cold_numbers.append(ball)
        
        return hot_numbers[:10], cold_numbers[:10]


def main():
    """主函数"""
    print("=" * 70)
    print("双色球 2026002 期号码推算")
    print("=" * 70)
    
    # 示例历史数据（最近30期）
    # 格式：(期号, [红球1-6], 蓝球)
    history_data = [
        ('2025124', [2, 5, 11, 19, 25, 32], 9),
        ('2025125', [7, 12, 15, 21, 28, 31], 4),
        ('2025126', [3, 8, 14, 22, 26, 33], 11),
        ('2025127', [1, 9, 16, 20, 27, 30], 6),
        ('2025128', [4, 10, 13, 23, 29, 31], 15),
        ('2025129', [6, 11, 17, 24, 28, 32], 8),
        ('2025130', [2, 8, 14, 19, 25, 30], 12),
        ('2025131', [5, 9, 15, 21, 27, 33], 3),
        ('2025132', [1, 7, 16, 22, 26, 31], 10),
        ('2025133', [3, 10, 13, 20, 29, 32], 5),
        ('2025134', [4, 11, 14, 23, 28, 30], 14),
        ('2025135', [6, 8, 17, 19, 25, 33], 7),
        ('2025136', [2, 9, 12, 21, 27, 31], 16),
        ('2025137', [5, 7, 15, 22, 26, 32], 2),
        ('2025138', [1, 10, 16, 20, 29, 30], 13),
        ('2025139', [3, 11, 13, 24, 28, 33], 9),
        ('2025140', [4, 8, 14, 19, 25, 31], 6),
        ('2025141', [6, 9, 17, 21, 27, 32], 11),
        ('2025142', [2, 7, 12, 23, 26, 30], 4),
        ('2025143', [5, 10, 15, 20, 29, 33], 8),
        ('2025144', [1, 11, 16, 22, 28, 31], 15),
        ('2025145', [3, 8, 13, 19, 25, 32], 12),
        ('2025146', [4, 9, 14, 21, 27, 30], 5),
        ('2025147', [6, 7, 17, 24, 26, 33], 10),
        ('2025148', [2, 10, 12, 20, 29, 31], 3),
        ('2025149', [5, 11, 15, 23, 28, 32], 14),
        ('2025150', [1, 8, 16, 19, 25, 30], 7),
        ('2025151', [3, 9, 13, 22, 27, 33], 16),
        ('2025152', [4, 7, 14, 21, 26, 31], 2),
        ('2026001', [6, 10, 17, 20, 29, 32], 13),  # 上一期
    ]
    
    print(f"\n📅 分析周期：{history_data[0][0]} ~ {history_data[-1][0]}")
    print(f"📊 历史期数：{len(history_data)} 期")
    
    # 创建分析器
    analyzer = LotteryAnalyzer()
    analyzer.load_history_data(history_data)
    
    # 分析24码
    codes_24 = analyzer.analyze_24_codes()
    
    # 分析热号冷号
    print(f"\n🔥 热号分析（最近30期出现频率最高）")
    hot_numbers, cold_numbers = analyzer.analyze_hot_cold_numbers()
    print(f"TOP10热号: {', '.join([f'{x:02d}' for x in hot_numbers])}")
    print(f"TOP10冷号: {', '.join([f'{x:02d}' for x in cold_numbers])}")
    
    # 生成投注方案
    scheme = analyzer.generate_betting_scheme('2026002', codes_24, num_bets=10)
    
    # 推荐方案
    print(f"\n💡 智能推荐（基于统计分析）")
    print("=" * 70)
    
    # 推荐1：热号组合
    hot_combo = random.sample([n for n in codes_24 if n in hot_numbers], min(6, len([n for n in codes_24 if n in hot_numbers])))
    while len(hot_combo) < 6:
        hot_combo.append(random.choice([n for n in codes_24 if n not in hot_combo]))
    hot_combo.sort()
    
    print(f"推荐1（热号组合）: {' '.join([f'{x:02d}' for x in hot_combo])} + {random.randint(1, 16):02d}")
    
    # 推荐2：冷热搭配
    mixed_combo = random.sample(hot_numbers[:5], 3)
    mixed_combo.extend(random.sample([n for n in codes_24 if n not in hot_numbers[:5]], 3))
    mixed_combo.sort()
    
    print(f"推荐2（冷热搭配）: {' '.join([f'{x:02d}' for x in mixed_combo])} + {random.randint(1, 16):02d}")
    
    # 推荐3：均衡组合
    balanced_combo = []
    # 从24码中均匀选择
    step = len(codes_24) // 6
    for i in range(6):
        idx = min(i * step, len(codes_24) - 1)
        balanced_combo.append(codes_24[idx])
    balanced_combo.sort()
    
    print(f"推荐3（均衡组合）: {' '.join([f'{x:02d}' for x in balanced_combo])} + {random.randint(1, 16):02d}")
    
    print("=" * 70)
    
    # 免责声明
    print(f"\n⚠️  重要提示")
    print("=" * 70)
    print("1. 以上号码仅基于历史数据统计分析生成，仅供参考")
    print("2. 双色球是完全随机的游戏，任何分析方法都无法预测开奖结果")
    print("3. 历史统计不代表未来趋势，过往数据不保证未来表现")
    print("4. 请理性投注，量力而行，不要沉迷")
    print("5. 本工具不对任何投注结果负责")
    print("=" * 70)
    
    print(f"\n✅ 分析完成！祝您好运！🍀")
    print("=" * 70)


if __name__ == "__main__":
    random.seed()  # 使用系统时间作为随机种子
    main()
