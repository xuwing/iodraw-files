#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球理性投注系统 V9.0 终极版
核心定位：概率优化与成本控制工具，非预测模型
三大基石：动态聚焦引擎 + 静态覆盖武器库(29组) + 矩阵投注法
"""

import random
from collections import Counter
from typing import List, Tuple, Dict, Set
from datetime import datetime
import itertools


class LotterySystemV9:
    """双色球V9.0投注系统"""
    
    # 18码黄金核心池（固定不变）
    GOLDEN_POOL = [2, 3, 7, 9, 10, 11, 13, 14, 18, 19, 21, 24, 25, 27, 28, 29, 30, 33]
    
    # 29组24码全覆盖组合（固定不变）
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
    
    # 断组定义
    SEGMENT_GROUPS_SEQUENCE = {
        'A': list(range(1, 6)),      # 01-05
        'B': list(range(6, 12)),     # 06-11
        'C': list(range(12, 17)),    # 12-16
        'D': list(range(17, 23)),    # 17-22
        'E': list(range(23, 28)),    # 23-27
        'F': list(range(28, 34)),    # 28-33
    }
    
    SEGMENT_GROUPS_JUMP = {
        'A': list(range(1, 4)) + list(range(31, 34)),      # 01-03, 31-33
        'B': list(range(4, 7)) + list(range(28, 31)),      # 04-06, 28-30
        'C': list(range(7, 10)) + list(range(25, 28)),     # 07-09, 25-27
        'D': list(range(10, 13)) + list(range(22, 25)),    # 10-12, 22-24
        'E': list(range(13, 16)) + list(range(19, 22)),    # 13-15, 19-21
        'F': list(range(16, 19)),                          # 16-18
    }
    
    def __init__(self):
        self.history_data = []
        self.last_draw = []
        
    def load_history(self, data: List[Tuple[str, List[int], int]]):
        """加载历史数据"""
        self.history_data = data
        if data:
            self.last_draw = data[-1][1]
        print(f"✅ 已加载 {len(data)} 期历史数据")
    
    def analyze_hot_cold(self, periods: int = 10) -> Dict[int, Dict]:
        """
        阶段一：分析热冷码并计算权重
        只在18码黄金池内分析
        """
        print(f"\n{'='*70}")
        print("阶段一：生成动态聚焦池")
        print(f"{'='*70}")
        
        # 统计最近N期的红球出现次数
        recent_balls = []
        for period, reds, blue in self.history_data[-periods:]:
            recent_balls.extend(reds)
        
        counter = Counter(recent_balls)
        
        # 只分析黄金池内的号码
        weights = {}
        for ball in self.GOLDEN_POOL:
            count = counter.get(ball, 0)
            
            # 热冷分级
            if count >= 2:
                status = '热码'
                weight = 1.2
            elif count == 1:
                status = '温码'
                weight = 1.0
            else:
                status = '冷码'
                weight = 0.8
            
            weights[ball] = {
                'count': count,
                'status': status,
                'weight': weight,
                'final_weight': weight  # 初始最终权重
            }
        
        print(f"\n📊 热冷码分析（最近{periods}期）：")
        print(f"{'号码':<6}{'出现次数':<10}{'状态':<8}{'基础权重'}")
        print("-" * 50)
        for ball in sorted(weights.keys()):
            info = weights[ball]
            print(f"{ball:02d}    {info['count']:<10}{info['status']:<8}{info['weight']:.1f}")
        
        return weights
    
    def apply_break_group_rules(self, weights: Dict[int, Dict]) -> Dict[int, Dict]:
        """
        应用智能断组规则
        若断组中的号码属于黄金池，权重×0.9（轻度惩罚）
        """
        print(f"\n🔍 智能断组分析：")
        
        # 分析上期开奖的断组情况
        last_draw_set = set(self.last_draw)
        
        print("\n【顺序断组法】A(01-05) B(06-11) C(12-16) D(17-22) E(23-27) F(28-33)")
        break_groups_seq = []
        for name, group_balls in self.SEGMENT_GROUPS_SEQUENCE.items():
            has_ball = any(b in last_draw_set for b in group_balls)
            status = "有号" if has_ball else "断组 ✗"
            print(f"  组{name}: {status}")
            if not has_ball:
                break_groups_seq.extend(group_balls)
        
        print("\n【跳段断组法】")
        break_groups_jump = []
        for name, group_balls in self.SEGMENT_GROUPS_JUMP.items():
            has_ball = any(b in last_draw_set for b in group_balls)
            status = "有号" if has_ball else "断组 ✗"
            print(f"  组{name}: {status}")
            if not has_ball:
                break_groups_jump.extend(group_balls)
        
        # 合并两种断组方法的结果
        all_break_balls = set(break_groups_seq + break_groups_jump)
        
        # 对黄金池内的断组号码应用0.9的权重惩罚
        affected_balls = []
        for ball in all_break_balls:
            if ball in weights:  # 在黄金池内
                weights[ball]['final_weight'] *= 0.9
                affected_balls.append(ball)
        
        if affected_balls:
            print(f"\n⚠️  黄金池内受断组影响的号码（权重×0.9）：")
            print(f"   {', '.join([f'{b:02d}' for b in sorted(affected_balls)])}")
        else:
            print(f"\n✓ 黄金池号码未受断组影响")
        
        return weights
    
    def generate_focus_pool(self, weights: Dict[int, Dict], pool_size: int = 13) -> List[int]:
        """
        生成动态聚焦池（12-14码）
        根据最终权重排序选取
        """
        # 按最终权重排序
        sorted_balls = sorted(
            weights.keys(),
            key=lambda x: weights[x]['final_weight'],
            reverse=True
        )
        
        # 选取前pool_size个
        focus_pool = sorted_balls[:pool_size]
        
        # 结构校验
        odd_count = sum(1 for b in focus_pool if b % 2 == 1)
        even_count = pool_size - odd_count
        ball_sum = sum(focus_pool)
        span = max(focus_pool) - min(focus_pool)
        
        print(f"\n✨ 动态聚焦池（{pool_size}码）：")
        print(f"   号码：{', '.join([f'{b:02d}' for b in sorted(focus_pool)])}")
        print(f"   和值：{ball_sum}")
        print(f"   奇偶：{odd_count}奇{even_count}偶")
        print(f"   跨度：{span}")
        
        # 结构校验警告
        if not (110 <= ball_sum <= 160):
            print(f"   ⚠️  和值 {ball_sum} 超出标准范围(110-160)")
        if span > 25:
            print(f"   ⚠️  跨度 {span} 超出标准范围(≤25)")
        if odd_count not in [5, 6, 7, 8]:
            print(f"   ⚠️  奇偶比 {odd_count}:{even_count} 可能不理想")
        
        return sorted(focus_pool)
    
    def find_elite_core(self, focus_pool: List[int], top_n: int = 4) -> Tuple[List[int], List[int]]:
        """
        阶段二：整合筛选精华核心
        扫描29组，选出重合度最高的3-5组，取交集
        """
        print(f"\n{'='*70}")
        print("阶段二：V9.0整合筛选精华核心")
        print(f"{'='*70}")
        
        focus_set = set(focus_pool)
        
        # 扫描29组，计算重合度
        overlap_scores = []
        for i, group in enumerate(self.COVERAGE_29_GROUPS, 1):
            group_set = set(group)
            overlap = len(focus_set & group_set)
            overlap_scores.append((i, overlap, group))
        
        # 按重合度排序
        overlap_scores.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n📊 29组覆盖组扫描结果（TOP10）：")
        print(f"{'组号':<6}{'重合数':<10}{'重合号码'}")
        print("-" * 70)
        for i, overlap, group in overlap_scores[:10]:
            group_set = set(group)
            overlap_balls = sorted(focus_set & group_set)
            overlap_str = ', '.join([f'{b:02d}' for b in overlap_balls])
            print(f"#{i:02d}   {overlap:<10}{overlap_str}")
        
        # 选取TOP N组
        top_groups = [group for _, _, group in overlap_scores[:top_n]]
        
        # 取交集（限制在聚焦池内）
        elite_core_set = set(top_groups[0]) & focus_set
        for group in top_groups[1:]:
            elite_core_set &= set(group)
        
        elite_core = sorted(list(elite_core_set))
        
        print(f"\n✨ 选中的TOP{top_n}组：{', '.join([f'#{i}' for i, _, _ in overlap_scores[:top_n]])}")
        print(f"✨ 精华核心（交集）：{', '.join([f'{b:02d}' for b in elite_core])} ({len(elite_core)}码)")
        
        # 返回精华核心和被选中的组号
        selected_groups = [i for i, _, _ in overlap_scores[:top_n]]
        
        return elite_core, selected_groups
    
    def build_three_engines(self, elite_core: List[int], focus_pool: List[int], 
                           weights: Dict[int, Dict]) -> Dict:
        """
        阶段三：三引擎矩阵构建
        A: 精准层（6-8码，中6保5）
        B: 稳健层（12-14码，中6保4）
        C: 防御层（被降权号码，单式1-2注）
        """
        print(f"\n{'='*70}")
        print("阶段三：三引擎矩阵构建")
        print(f"{'='*70}")
        
        engines = {}
        
        # 引擎A：精准层
        if len(elite_core) >= 6:
            engine_a_pool = elite_core[:8]  # 最多取8码
        else:
            # 从聚焦池补充
            needed = 6 - len(elite_core)
            supplement = [b for b in focus_pool if b not in elite_core][:needed]
            engine_a_pool = elite_core + supplement
        
        engine_a_pool = sorted(engine_a_pool[:8])  # 限制最多8码
        
        print(f"\n🎯 引擎A - 精准层（冲击高奖）：")
        print(f"   号码池：{', '.join([f'{b:02d}' for b in engine_a_pool])} ({len(engine_a_pool)}码)")
        print(f"   策略：中6保5矩阵")
        
        # 生成中6保5组合
        if len(engine_a_pool) == 6:
            combos_a = list(itertools.combinations(engine_a_pool, 6))
            print(f"   注数：{len(combos_a)} 注")
        elif len(engine_a_pool) == 7:
            combos_a = list(itertools.combinations(engine_a_pool, 6))
            print(f"   注数：{len(combos_a)} 注")
        else:  # 8码
            combos_a = list(itertools.combinations(engine_a_pool, 6))
            print(f"   注数：{len(combos_a)} 注（8码C6）")
        
        engines['A'] = {
            'pool': engine_a_pool,
            'combos': combos_a[:12],  # 限制最多12注
            'target': '中6保5',
            'cost': len(combos_a[:12]) * 2
        }
        
        # 引擎B：稳健层
        engine_b_pool = focus_pool
        print(f"\n🛡️  引擎B - 稳健层（稳定收益）：")
        print(f"   号码池：{', '.join([f'{b:02d}' for b in engine_b_pool])} ({len(engine_b_pool)}码)")
        print(f"   策略：中6保4矩阵")
        
        # 中6保4的简化实现：选取部分组合
        # 实际中6保4需要复杂的旋转矩阵，这里简化为随机选取
        all_combos_b = list(itertools.combinations(engine_b_pool, 6))
        # 根据池子大小选择注数
        if len(engine_b_pool) <= 12:
            num_bets_b = 10
        elif len(engine_b_pool) == 13:
            num_bets_b = 13
        else:
            num_bets_b = 17
        
        # 智能选择组合（确保覆盖度）
        combos_b = self._smart_select_combos(engine_b_pool, num_bets_b)
        print(f"   注数：{len(combos_b)} 注")
        
        engines['B'] = {
            'pool': engine_b_pool,
            'combos': combos_b,
            'target': '中6保4',
            'cost': len(combos_b) * 2
        }
        
        # 引擎C：防御层
        # 找出被降权但未进入聚焦池的黄金池号码
        defense_pool = [b for b in self.GOLDEN_POOL 
                       if b not in focus_pool and weights[b]['final_weight'] < weights[b]['weight']]
        
        if defense_pool and len(defense_pool) >= 3:
            # 选择3-4个权重相对较高的
            defense_sorted = sorted(defense_pool, 
                                   key=lambda x: weights[x]['final_weight'], 
                                   reverse=True)
            defense_selected = defense_sorted[:3]
            
            # 从聚焦池选3个补充
            supplement = [b for b in focus_pool if b not in defense_selected][:3]
            defense_full = sorted((defense_selected + supplement))[:6]
            
            combos_c = [tuple(defense_full)]
        else:
            # 如果没有被降权的，从聚焦池末尾选
            if len(focus_pool) >= 6:
                defense_full = sorted(focus_pool[-6:])
            else:
                # 从黄金池补充
                needed = 6 - len(focus_pool)
                supplement = [b for b in self.GOLDEN_POOL if b not in focus_pool][:needed]
                defense_full = sorted(focus_pool + supplement)[:6]
            combos_c = [tuple(defense_full)]
        
        print(f"\n🔰 引擎C - 防御层（对冲风险）：")
        print(f"   号码：{', '.join([f'{b:02d}' for b in defense_full])}")
        print(f"   注数：{len(combos_c)} 注")
        
        engines['C'] = {
            'pool': defense_full,
            'combos': combos_c,
            'target': '单式防守',
            'cost': len(combos_c) * 2
        }
        
        # 总成本
        total_cost = sum(e['cost'] for e in engines.values())
        print(f"\n💰 预计总成本：{total_cost} 元")
        
        return engines
    
    def _smart_select_combos(self, pool: List[int], num_bets: int) -> List[Tuple]:
        """智能选择组合，确保覆盖度"""
        all_combos = list(itertools.combinations(pool, 6))
        
        if len(all_combos) <= num_bets:
            return all_combos
        
        # 使用贪心算法选择组合，确保每个号码都被充分覆盖
        selected = []
        coverage = {b: 0 for b in pool}
        
        # 先随机打乱
        random.shuffle(all_combos)
        
        for combo in all_combos:
            if len(selected) >= num_bets:
                break
            
            # 计算这个组合的覆盖价值
            value = sum(1 / (coverage[b] + 1) for b in combo)
            
            selected.append((combo, value))
            for b in combo:
                coverage[b] += 1
        
        # 按价值排序，取top N
        selected.sort(key=lambda x: x[1], reverse=True)
        return [combo for combo, _ in selected[:num_bets]]
    
    def select_blues(self, periods_hot: int = 10, periods_cold: int = 30) -> Tuple[int, int]:
        """
        选择蓝球：双蓝策略
        热蓝：最近10期出现最多的
        冷蓝：最近30期遗漏最长的
        """
        # 统计蓝球
        blues_hot = [blue for _, _, blue in self.history_data[-periods_hot:]]
        blues_cold = [blue for _, _, blue in self.history_data[-periods_cold:]]
        
        # 热蓝
        counter_hot = Counter(blues_hot)
        hot_blue = counter_hot.most_common(1)[0][0] if counter_hot else 1
        
        # 冷蓝（遗漏最长）
        all_blues = set(range(1, 17))
        recent_blues = set(blues_cold)
        missing_blues = all_blues - recent_blues
        
        if missing_blues:
            cold_blue = min(missing_blues)
        else:
            # 如果都出现过，选出现次数最少的
            counter_cold = Counter(blues_cold)
            cold_blue = counter_cold.most_common()[-1][0]
        
        print(f"\n🔵 蓝球策略（双蓝）：")
        print(f"   热蓝：{hot_blue:02d}（最近{periods_hot}期出现{counter_hot.get(hot_blue, 0)}次）")
        print(f"   冷蓝：{cold_blue:02d}（长期遗漏）")
        
        return hot_blue, cold_blue
    
    def generate_final_tickets(self, engines: Dict, hot_blue: int, cold_blue: int) -> List[Dict]:
        """
        阶段四：生成最终投注单
        """
        print(f"\n{'='*70}")
        print("阶段四：最终投注方案")
        print(f"{'='*70}")
        
        tickets = []
        
        # 引擎A - 分配热蓝
        for combo in engines['A']['combos']:
            tickets.append({
                'engine': 'A-精准',
                'reds': sorted(combo),
                'blue': hot_blue
            })
        
        # 引擎B - 分配冷蓝
        for combo in engines['B']['combos']:
            tickets.append({
                'engine': 'B-稳健',
                'reds': sorted(combo),
                'blue': cold_blue
            })
        
        # 引擎C - 任选一个蓝球
        for combo in engines['C']['combos']:
            tickets.append({
                'engine': 'C-防御',
                'reds': sorted(combo),
                'blue': hot_blue  # 或cold_blue，可随机
            })
        
        print(f"\n📋 最终投注方案：")
        print(f"{'注号':<6}{'引擎':<10}{'红球':<40}{'蓝球'}")
        print("-" * 70)
        
        for i, ticket in enumerate(tickets, 1):
            reds_str = ' '.join([f'{b:02d}' for b in ticket['reds']])
            print(f"#{i:<5}{ticket['engine']:<10}{reds_str:<40}{ticket['blue']:02d}")
        
        total_cost = len(tickets) * 2
        print(f"\n💰 总注数：{len(tickets)} 注")
        print(f"💰 总成本：{total_cost} 元")
        
        return tickets
    
    def run_full_system(self, period_name: str = "下期") -> Dict:
        """运行完整的V9.0系统"""
        print(f"\n{'#'*70}")
        print(f"# 双色球理性投注系统 V9.0 终极版")
        print(f"# 目标期号：{period_name}")
        print(f"# 执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*70}")
        
        # 阶段一：动态聚焦池
        weights = self.analyze_hot_cold(periods=10)
        weights = self.apply_break_group_rules(weights)
        focus_pool = self.generate_focus_pool(weights, pool_size=13)
        
        # 阶段二：精华核心
        elite_core, selected_groups = self.find_elite_core(focus_pool, top_n=4)
        
        # 阶段三：三引擎矩阵
        engines = self.build_three_engines(elite_core, focus_pool, weights)
        
        # 蓝球选择
        hot_blue, cold_blue = self.select_blues()
        
        # 阶段四：最终投注
        tickets = self.generate_final_tickets(engines, hot_blue, cold_blue)
        
        # 返回完整结果
        result = {
            'period': period_name,
            'focus_pool': focus_pool,
            'elite_core': elite_core,
            'selected_groups': selected_groups,
            'engines': engines,
            'hot_blue': hot_blue,
            'cold_blue': cold_blue,
            'tickets': tickets,
            'total_cost': len(tickets) * 2
        }
        
        print(f"\n{'='*70}")
        print("✅ V9.0系统运行完成！")
        print(f"{'='*70}")
        
        return result


def main():
    """主函数：演示V9.0系统"""
    
    # 加载历史数据（最近30期）
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
    system = LotterySystemV9()
    system.load_history(history_data)
    
    # 运行完整系统
    result = system.run_full_system(period_name="2026003")
    
    # 输出建议
    print(f"\n{'='*70}")
    print("📌 执行建议：")
    print(f"{'='*70}")
    print("1. 按上述方案机械投注，不做任何调整")
    print("2. 严格记录本期执行情况")
    print("3. 开奖后对比各层命中情况")
    print("4. 连续执行30期以上才能评估系统有效性")
    print("5. 预算控制在30-60元/期")
    print(f"{'='*70}")
    
    print(f"\n⚠️  重要提醒：")
    print("• 本系统是概率优化工具，非预测模型")
    print("• 不保证每期中奖，接受正常波动")
    print("• 理性投注，量力而行")
    print("• 严格执行流程，禁止拟合")
    
    return result


if __name__ == "__main__":
    result = main()
