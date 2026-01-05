#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球理性投注系统 V9.1 优化版
核心优化：动态池+改进权重+弱化断组+并集核心+增加注数
目标：提升5红和6红命中概率
"""

import random
from collections import Counter
from typing import List, Tuple, Dict, Set
from datetime import datetime
import itertools


class LotterySystemV91:
    """双色球V9.1优化系统"""
    
    # 29组24码全覆盖组合（保持不变）
    COVERAGE_29_GROUPS = [
        [1, 2, 3, 5, 7, 9, 10, 11, 12, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 28, 30, 32, 33],
        [1, 2, 4, 5, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 22, 23, 25, 26, 27, 28, 29, 30, 32],
        [1, 2, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        [3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 17, 18, 20, 21, 22, 23, 24, 26, 27, 29, 30, 32, 33],
        [1, 3, 4, 6, 7, 8, 9, 11, 13, 14, 17, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29, 31, 32, 33],
        [1, 2, 3, 4, 5, 8, 9, 10, 12, 13, 14, 15, 16, 18, 20, 22, 23, 25, 26, 27, 28, 29, 30, 33],
        [1, 2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 16, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33],
        [1, 2, 3, 4, 5, 7, 8, 11, 13, 14, 15, 16, 17, 18, 20, 21, 24, 25, 27, 28, 29, 30, 32, 33],
        [1, 2, 3, 4, 6, 8, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 31, 33],
        [2, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 29, 30, 31, 32],
        [1, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 19, 20, 21, 22, 23, 24, 26, 27, 28, 30, 31, 33],
        [2, 3, 5, 6, 7, 8, 9, 10, 12, 15, 16, 17, 18, 19, 20, 22, 23, 25, 26, 29, 30, 31, 32, 33],
        [1, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 17, 18, 19, 20, 26, 27, 28, 29, 30, 31, 32, 33],
        [1, 2, 3, 6, 7, 8, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 24, 25, 26, 28, 29, 31, 32, 33],
        [1, 2, 3, 5, 6, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20, 21, 24, 25, 26, 28, 29, 30, 31, 33],
        [1, 2, 3, 6, 7, 8, 9, 11, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 31, 32, 33],
        [1, 3, 5, 6, 7, 8, 9, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 33],
        [1, 3, 6, 7, 8, 9, 10, 11, 12, 14, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28, 29, 31, 32, 33],
        [1, 2, 3, 6, 8, 9, 10, 11, 12, 14, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 31, 33],
        [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 29, 31, 32],
        [1, 2, 4, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 19, 22, 23, 25, 26, 27, 28, 30, 31, 32],
        [1, 2, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 22, 23, 25, 27, 28, 29, 30, 31, 32],
        [1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 22, 23, 25, 26, 27, 28, 29, 30, 31],
        [1, 2, 4, 5, 6, 7, 9, 11, 13, 14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 27, 28, 30, 31, 32],
        [1, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 21, 24, 26, 27, 28, 29, 30, 31, 32],
        [1, 2, 3, 4, 5, 6, 7, 9, 13, 14, 15, 16, 17, 19, 20, 22, 23, 25, 27, 28, 30, 31, 32, 33],
        [2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 16, 17, 18, 19, 20, 22, 23, 25, 26, 27, 29, 31, 32, 33],
        [2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 24, 25, 26, 27, 30, 31, 32, 33],
        [2, 3, 4, 5, 6, 8, 9, 11, 13, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 33],
    ]
    
    # 跳段断组（弱化断组规则，仅保留跳段）
    SEGMENT_GROUPS_JUMP = {
        'A': list(range(1, 4)) + list(range(31, 34)),
        'B': list(range(4, 7)) + list(range(28, 31)),
        'C': list(range(7, 10)) + list(range(25, 28)),
        'D': list(range(10, 13)) + list(range(22, 25)),
        'E': list(range(13, 16)) + list(range(19, 22)),
        'F': list(range(16, 19)),
    }
    
    def __init__(self):
        self.history_data = []
        self.last_draw = []
        self.dynamic_pool = []
        
    def load_history(self, data: List[Tuple[str, List[int], int]]):
        """加载历史数据"""
        self.history_data = data
        if data:
            self.last_draw = data[-1][1]
        print(f"✅ 已加载 {len(data)} 期历史数据")
    
    def generate_dynamic_pool(self, periods: int = 30) -> List[int]:
        """
        生成动态黄金池（V9.1核心优化）
        基于最近N期统计，取TOP22码
        """
        # 统计最近N期红球出现次数
        recent_balls = []
        for period, reds, blue in self.history_data[-periods:]:
            recent_balls.extend(reds)
        
        counter = Counter(recent_balls)
        
        # 按频率排序，取TOP22
        sorted_balls = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        dynamic_pool = [ball for ball, count in sorted_balls[:22]]
        
        self.dynamic_pool = sorted(dynamic_pool)
        
        print(f"\n📊 动态黄金池（22码，基于最近{periods}期）：")
        print(f"   {', '.join([f'{b:02d}' for b in self.dynamic_pool])}")
        print(f"\n   出现频率分布：")
        for i, (ball, count) in enumerate(sorted_balls[:22], 1):
            freq = count / periods * 100
            print(f"   {i:2d}. {ball:02d}号: {count:2d}次 ({freq:5.1f}%)")
        
        return self.dynamic_pool
    
    def analyze_hot_cold_v2(self, periods: int = 10) -> Dict[int, Dict]:
        """
        改进的热冷码分析（V9.1优化）
        使用加权指数衰减模型
        """
        print(f"\n{'='*70}")
        print("阶段一：生成动态聚焦池（V9.1优化版）")
        print(f"{'='*70}")
        
        # 使用指数衰减权重
        decay_factor = 0.9
        weights = {}
        
        # 只分析动态池内的号码
        for ball in self.dynamic_pool:
            score = 0.0
            # 从最近期开始往前统计
            for i in range(periods):
                period_reds = self.history_data[-(i+1)][1]
                if ball in period_reds:
                    score += (decay_factor ** i)
            
            # 归一化
            weight = 0.8 + (score / periods) * 0.4  # 权重范围0.8-1.2
            
            weights[ball] = {
                'score': score,
                'weight': weight,
                'final_weight': weight
            }
        
        print(f"\n📊 热冷码分析（指数衰减模型，最近{periods}期）：")
        print(f"{'号码':<6}{'得分':<10}{'权重'}")
        print("-" * 50)
        sorted_weights = sorted(weights.items(), key=lambda x: x[1]['score'], reverse=True)
        for ball, info in sorted_weights[:15]:
            print(f"{ball:02d}    {info['score']:<10.2f}{info['weight']:.3f}")
        
        return weights
    
    def apply_weak_break_rules(self, weights: Dict[int, Dict]) -> Dict[int, Dict]:
        """
        弱化的断组规则（V9.1优化）
        仅对连续2期断组的号码轻微降权×0.95
        """
        print(f"\n🔍 弱化断组分析（仅跳段法，连续2期断组）：")
        
        # 检查最近2期的断组情况
        last_2_draws = [self.history_data[-2][1], self.history_data[-1][1]]
        
        continuous_break = []
        for name, group_balls in self.SEGMENT_GROUPS_JUMP.items():
            # 检查两期是否都断组
            break_count = 0
            for draw in last_2_draws:
                if not any(b in draw for b in group_balls):
                    break_count += 1
            
            if break_count == 2:  # 连续2期断组
                print(f"  组{name}: 连续2期断组 ✗✗")
                continuous_break.extend(group_balls)
            else:
                print(f"  组{name}: 正常")
        
        # 对连续断组的号码轻微降权
        affected = []
        for ball in continuous_break:
            if ball in weights:
                weights[ball]['final_weight'] *= 0.95
                affected.append(ball)
        
        if affected:
            print(f"\n⚠️  受连续断组影响的号码（权重×0.95）：")
            print(f"   {', '.join([f'{b:02d}' for b in sorted(affected)])}")
        else:
            print(f"\n✓ 无连续断组影响")
        
        return weights
    
    def generate_focus_pool_v2(self, weights: Dict[int, Dict], pool_size: int = 15) -> List[int]:
        """
        生成增强的动态聚焦池（V9.1优化）
        扩大到15码
        """
        sorted_balls = sorted(
            weights.keys(),
            key=lambda x: weights[x]['final_weight'],
            reverse=True
        )
        
        focus_pool = sorted_balls[:pool_size]
        
        # 结构校验
        odd_count = sum(1 for b in focus_pool if b % 2 == 1)
        even_count = pool_size - odd_count
        ball_sum = sum(focus_pool)
        span = max(focus_pool) - min(focus_pool) if focus_pool else 0
        
        print(f"\n✨ 动态聚焦池（{pool_size}码）：")
        print(f"   号码：{', '.join([f'{b:02d}' for b in sorted(focus_pool)])}")
        print(f"   和值：{ball_sum}")
        print(f"   奇偶：{odd_count}奇{even_count}偶")
        print(f"   跨度：{span}")
        
        # 结构校验
        warnings = []
        if not (110 <= ball_sum <= 160):
            warnings.append(f"和值{ball_sum}超出标准范围(110-160)")
        if span > 25:
            warnings.append(f"跨度{span}超出标准范围(≤25)")
        
        if warnings:
            for w in warnings:
                print(f"   ⚠️  {w}")
        else:
            print(f"   ✓ 结构校验通过")
        
        return sorted(focus_pool)
    
    def find_elite_core_v2(self, focus_pool: List[int], top_n: int = 8) -> Tuple[List[int], List[int]]:
        """
        改进的精华核心算法（V9.1核心优化）
        使用加权并集而非交集
        """
        print(f"\n{'='*70}")
        print("阶段二：V9.1精华核心筛选（并集算法）")
        print(f"{'='*70}")
        
        focus_set = set(focus_pool)
        
        # 扫描29组
        overlap_scores = []
        for i, group in enumerate(self.COVERAGE_29_GROUPS, 1):
            group_set = set(group)
            overlap = len(focus_set & group_set)
            overlap_scores.append((i, overlap, group))
        
        overlap_scores.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n📊 29组覆盖组扫描结果（TOP{top_n}）：")
        print(f"{'组号':<6}{'重合数':<10}{'重合号码'}")
        print("-" * 70)
        for i, overlap, group in overlap_scores[:top_n]:
            group_set = set(group)
            overlap_balls = sorted(focus_set & group_set)
            overlap_str = ', '.join([f'{b:02d}' for b in overlap_balls])
            print(f"#{i:02d}   {overlap:<10}{overlap_str}")
        
        # 选取TOP N组
        top_groups = [group for _, _, group in overlap_scores[:top_n]]
        selected_groups = [i for i, _, _ in overlap_scores[:top_n]]
        
        # 统计出现次数（并集）
        ball_frequency = Counter()
        for group in top_groups:
            for ball in group:
                if ball in focus_set:  # 限制在聚焦池内
                    ball_frequency[ball] += 1
        
        # 选出出现次数≥阈值的号码
        threshold = max(4, top_n // 2)  # 至少一半的组包含
        elite_core = [ball for ball, count in ball_frequency.items() if count >= threshold]
        
        # 如果不足8码，按频率补充
        if len(elite_core) < 8:
            additional = [ball for ball, count in ball_frequency.most_common() if ball not in elite_core]
            elite_core.extend(additional[:8 - len(elite_core)])
        
        elite_core = sorted(elite_core[:10])  # 最多10码
        
        print(f"\n✨ 选中的TOP{top_n}组：{', '.join([f'#{i}' for i in selected_groups])}")
        print(f"✨ 精华核心（出现≥{threshold}次）：{', '.join([f'{b:02d}' for b in elite_core])} ({len(elite_core)}码)")
        
        return elite_core, selected_groups
    
    def build_three_engines_v2(self, elite_core: List[int], focus_pool: List[int], 
                               weights: Dict[int, Dict]) -> Dict:
        """
        优化的三引擎矩阵（V9.1优化）
        增加总注数，优化分配
        """
        print(f"\n{'='*70}")
        print("阶段三：三引擎矩阵构建（V9.1优化版）")
        print(f"{'='*70}")
        
        engines = {}
        
        # 引擎A：精准层（增加到10-15注）
        if len(elite_core) >= 7:
            engine_a_pool = elite_core[:8]
        else:
            needed = 8 - len(elite_core)
            supplement = [b for b in focus_pool if b not in elite_core][:needed]
            engine_a_pool = sorted(elite_core + supplement)[:8]
        
        # 生成C7组合（7选6），约7注
        if len(engine_a_pool) >= 7:
            combos_a = list(itertools.combinations(engine_a_pool[:7], 6))
        else:
            combos_a = [tuple(engine_a_pool)]
        
        # 如果是8码，再加5注C8的部分组合
        if len(engine_a_pool) == 8:
            combos_a_extra = list(itertools.combinations(engine_a_pool, 6))[:5]
            combos_a.extend(combos_a_extra)
        
        combos_a = combos_a[:12]  # 最多12注
        
        print(f"\n🎯 引擎A - 精准层（冲击高奖）：")
        print(f"   号码池：{', '.join([f'{b:02d}' for b in engine_a_pool])} ({len(engine_a_pool)}码)")
        print(f"   策略：7选6组合")
        print(f"   注数：{len(combos_a)} 注")
        
        engines['A'] = {
            'pool': engine_a_pool,
            'combos': combos_a,
            'target': '中6保5',
            'cost': len(combos_a) * 2
        }
        
        # 引擎B：稳健层（增加到20-30注）
        engine_b_pool = focus_pool
        
        # 智能选择组合
        num_bets_b = 25  # 固定25注
        combos_b = self._smart_select_combos_v2(engine_b_pool, num_bets_b)
        
        print(f"\n🛡️  引擎B - 稳健层（稳定收益）：")
        print(f"   号码池：{', '.join([f'{b:02d}' for b in engine_b_pool])} ({len(engine_b_pool)}码)")
        print(f"   策略：智能旋转矩阵")
        print(f"   注数：{len(combos_b)} 注")
        
        engines['B'] = {
            'pool': engine_b_pool,
            'combos': combos_b,
            'target': '中6保4',
            'cost': len(combos_b) * 2
        }
        
        # 引擎C：防御层（冷号回补，增加到5-8注）
        # 找出不在聚焦池的动态池号码
        defense_pool = [b for b in self.dynamic_pool if b not in focus_pool]
        
        if len(defense_pool) >= 6:
            # 选择权重较低的号码（可能回补）
            defense_sorted = sorted(defense_pool, key=lambda x: weights.get(x, {}).get('final_weight', 0))
            defense_selected = defense_sorted[:9]  # 取9个冷号
            
            # 生成5-8注
            combos_c = []
            for _ in range(5):
                combo = random.sample(defense_selected, 6)
                combos_c.append(tuple(sorted(combo)))
        else:
            # 备用方案
            defense_full = sorted((self.dynamic_pool[-6:]))
            combos_c = [tuple(defense_full)]
        
        print(f"\n🔰 引擎C - 防御层（冷号回补）：")
        print(f"   冷号池：{', '.join([f'{b:02d}' for b in defense_selected if 'defense_selected' in locals()])} ")
        print(f"   注数：{len(combos_c)} 注")
        
        engines['C'] = {
            'pool': defense_selected if 'defense_selected' in locals() else self.dynamic_pool[-6:],
            'combos': combos_c,
            'target': '冷号回补',
            'cost': len(combos_c) * 2
        }
        
        # 总成本
        total_cost = sum(e['cost'] for e in engines.values())
        print(f"\n💰 预计总成本：{total_cost} 元（{sum(len(e['combos']) for e in engines.values())}注）")
        
        return engines
    
    def _smart_select_combos_v2(self, pool: List[int], num_bets: int) -> List[Tuple]:
        """优化的组合选择算法"""
        # 先生成候选组合
        all_combos = []
        attempts = min(1000, num_bets * 100)
        
        for _ in range(attempts):
            combo = tuple(sorted(random.sample(pool, 6)))
            
            # 多维度过滤
            if self._validate_combo_v2(combo):
                all_combos.append(combo)
            
            if len(all_combos) >= num_bets * 3:
                break
        
        # 去重
        all_combos = list(set(all_combos))
        
        # 贪心选择确保覆盖
        selected = []
        coverage = {b: 0 for b in pool}
        
        for combo in all_combos:
            if len(selected) >= num_bets:
                break
            
            # 计算覆盖价值
            value = sum(1 / (coverage[b] + 1) for b in combo)
            selected.append((combo, value))
            
            for b in combo:
                coverage[b] += 1
        
        # 按价值排序
        selected.sort(key=lambda x: x[1], reverse=True)
        return [combo for combo, _ in selected[:num_bets]]
    
    def _validate_combo_v2(self, combo: Tuple[int]) -> bool:
        """
        多维度组合验证（V9.1新增）
        """
        combo_list = list(combo)
        
        # 1. 和值验证
        combo_sum = sum(combo_list)
        if not (110 <= combo_sum <= 160):
            return False
        
        # 2. 跨度验证
        span = max(combo_list) - min(combo_list)
        if span > 28 or span < 18:
            return False
        
        # 3. 奇偶验证
        odd_count = sum(1 for n in combo_list if n % 2 == 1)
        if odd_count not in [2, 3, 4]:
            return False
        
        # 4. 连号验证
        consecutive = 0
        for i in range(5):
            if combo_list[i+1] - combo_list[i] == 1:
                consecutive += 1
        if consecutive > 2:
            return False
        
        return True
    
    def select_blues_v2(self, periods_hot: int = 5, periods_warm: int = 10, 
                        periods_cold: int = 30) -> Tuple[int, int, int]:
        """
        三蓝策略（V9.1优化）
        """
        blues_hot = [blue for _, _, blue in self.history_data[-periods_hot:]]
        blues_warm = [blue for _, _, blue in self.history_data[-periods_warm:]]
        blues_cold = [blue for _, _, blue in self.history_data[-periods_cold:]]
        
        # 热蓝
        counter_hot = Counter(blues_hot)
        hot_blue = counter_hot.most_common(1)[0][0] if counter_hot else 1
        
        # 温蓝
        counter_warm = Counter(blues_warm)
        sorted_warm = counter_warm.most_common()
        warm_blue = sorted_warm[len(sorted_warm)//2][0] if len(sorted_warm) > 2 else 8
        
        # 冷蓝
        all_blues = set(range(1, 17))
        recent_blues = set(blues_cold)
        missing_blues = all_blues - recent_blues
        
        if missing_blues:
            cold_blue = min(missing_blues)
        else:
            counter_cold = Counter(blues_cold)
            cold_blue = counter_cold.most_common()[-1][0]
        
        print(f"\n🔵 蓝球策略（三蓝）：")
        print(f"   热蓝：{hot_blue:02d}（最近{periods_hot}期最热）")
        print(f"   温蓝：{warm_blue:02d}（最近{periods_warm}期居中）")
        print(f"   冷蓝：{cold_blue:02d}（长期遗漏）")
        
        return hot_blue, warm_blue, cold_blue
    
    def generate_final_tickets_v2(self, engines: Dict, hot_blue: int, 
                                  warm_blue: int, cold_blue: int) -> List[Dict]:
        """生成最终投注单（V9.1优化）"""
        print(f"\n{'='*70}")
        print("阶段四：最终投注方案（V9.1优化版）")
        print(f"{'='*70}")
        
        tickets = []
        
        # 引擎A - 热蓝+温蓝交替
        for i, combo in enumerate(engines['A']['combos']):
            blue = hot_blue if i % 2 == 0 else warm_blue
            tickets.append({
                'engine': 'A-精准',
                'reds': sorted(combo),
                'blue': blue
            })
        
        # 引擎B - 温蓝+冷蓝交替
        for i, combo in enumerate(engines['B']['combos']):
            blue = warm_blue if i % 2 == 0 else cold_blue
            tickets.append({
                'engine': 'B-稳健',
                'reds': sorted(combo),
                'blue': blue
            })
        
        # 引擎C - 冷蓝
        for combo in engines['C']['combos']:
            tickets.append({
                'engine': 'C-防御',
                'reds': sorted(combo),
                'blue': cold_blue
            })
        
        print(f"\n📋 最终投注方案：")
        print(f"{'注号':<6}{'引擎':<10}{'红球':<40}{'蓝球'}")
        print("-" * 70)
        
        for i, ticket in enumerate(tickets, 1):
            reds_str = ' '.join([f'{b:02d}' for b in ticket['reds']])
            print(f"#{i:<5}{ticket['engine']:<10}{reds_str:<40}{ticket['blue']:02d}")
            
            if i == 10 or i == 35:  # 分隔不同引擎
                print("-" * 70)
        
        total_cost = len(tickets) * 2
        print(f"\n💰 总注数：{len(tickets)} 注")
        print(f"💰 总成本：{total_cost} 元")
        
        return tickets
    
    def run_full_system_v91(self, period_name: str = "下期") -> Dict:
        """运行完整的V9.1系统"""
        print(f"\n{'#'*70}")
        print(f"# 双色球理性投注系统 V9.1 优化版")
        print(f"# 目标期号：{period_name}")
        print(f"# 执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*70}")
        
        # 生成动态黄金池
        dynamic_pool = self.generate_dynamic_pool(periods=30)
        
        # 阶段一：动态聚焦池
        weights = self.analyze_hot_cold_v2(periods=10)
        weights = self.apply_weak_break_rules(weights)
        focus_pool = self.generate_focus_pool_v2(weights, pool_size=15)
        
        # 阶段二：精华核心
        elite_core, selected_groups = self.find_elite_core_v2(focus_pool, top_n=8)
        
        # 阶段三：三引擎矩阵
        engines = self.build_three_engines_v2(elite_core, focus_pool, weights)
        
        # 蓝球选择
        hot_blue, warm_blue, cold_blue = self.select_blues_v2()
        
        # 阶段四：最终投注
        tickets = self.generate_final_tickets_v2(engines, hot_blue, warm_blue, cold_blue)
        
        result = {
            'period': period_name,
            'dynamic_pool': dynamic_pool,
            'focus_pool': focus_pool,
            'elite_core': elite_core,
            'selected_groups': selected_groups,
            'engines': engines,
            'blues': {'hot': hot_blue, 'warm': warm_blue, 'cold': cold_blue},
            'tickets': tickets,
            'total_cost': len(tickets) * 2
        }
        
        print(f"\n{'='*70}")
        print("✅ V9.1系统运行完成！")
        print(f"{'='*70}")
        
        return result


def main():
    """主函数"""
    
    # 加载历史数据
    history_data = [
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
        ('2026001', [6, 10, 17, 20, 29, 32], 13),
        ('2026002', [1, 5, 7, 18, 30, 32], 2),
    ]
    
    # 创建系统实例
    system = LotterySystemV91()
    system.load_history(history_data)
    
    # 运行完整系统
    result = system.run_full_system_v91(period_name="2026003")
    
    # 输出建议
    print(f"\n{'='*70}")
    print("📌 V9.1版本改进总结：")
    print(f"{'='*70}")
    print("✅ 动态黄金池：22码（vs V9.0的18码固定池）")
    print("✅ 聚焦池扩大：15码（vs V9.0的13码）")
    print("✅ 精华核心优化：并集算法（vs V9.0的交集）")
    print("✅ 断组规则弱化：仅连续2期断组×0.95")
    print("✅ 总注数增加：40-45注（vs V9.0的15-26注）")
    print("✅ 成本提升：80-90元/期（vs V9.0的30-52元）")
    print("✅ 三蓝策略：热+温+冷（vs V9.0的双蓝）")
    print("✅ 多维度过滤：和值+跨度+奇偶+连号")
    print(f"{'='*70}\n")
    
    print("⚠️  重要提醒：")
    print("• V9.1成本是V9.0的约2倍")
    print("• 需要真实数据回测验证效果")
    print("• 理论上应提升5红和6红命中概率")
    print("• 仍需长期执行（100期以上）才能评估")
    
    return result


if __name__ == "__main__":
    result = main()
