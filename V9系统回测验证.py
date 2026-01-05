#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球V9.0系统 - 历史回测验证工具
目标：评估系统命中率，寻找优化空间
"""

import sys
import json
from collections import Counter, defaultdict
from typing import List, Tuple, Dict
from datetime import datetime


# 导入V9系统
sys.path.insert(0, '/home/engine/project')
from 双色球V9系统 import LotterySystemV9


class V9BacktestAnalyzer:
    """V9.0系统回测分析器"""
    
    def __init__(self):
        self.system = LotterySystemV9()
        self.results = []
        
    def load_historical_data(self, filepath: str = None) -> List[Tuple]:
        """
        加载历史数据
        如果没有文件，使用示例数据
        """
        # 这里应该加载真实的100期数据
        # 由于没有真实数据，我们使用模拟数据进行演示
        print("⚠️  注意：使用模拟数据进行回测演示")
        print("实际使用时请替换为真实的100期历史数据\n")
        
        # 模拟100期数据（实际应替换为真实数据）
        historical_data = self._generate_sample_data(100)
        
        return historical_data
    
    def _generate_sample_data(self, periods: int) -> List[Tuple]:
        """生成示例数据（实际应使用真实数据）"""
        import random
        data = []
        base_period = 2025000
        
        for i in range(periods):
            period_num = f"{base_period + i + 1}"
            # 生成符合规律的红球（从黄金池中随机选择为主）
            if random.random() < 0.7:  # 70%从黄金池
                reds = random.sample(self.system.GOLDEN_POOL, 4)
                others = random.sample([b for b in range(1, 34) if b not in self.system.GOLDEN_POOL], 2)
                reds.extend(others)
            else:
                reds = random.sample(range(1, 34), 6)
            
            reds = sorted(reds)
            blue = random.randint(1, 16)
            data.append((period_num, reds, blue))
        
        return data
    
    def backtest_single_period(self, test_period: int, all_data: List[Tuple]) -> Dict:
        """
        回测单期
        test_period: 要测试的期数索引
        all_data: 所有历史数据
        """
        # 使用前30期数据作为训练数据
        if test_period < 30:
            return None
        
        train_data = all_data[test_period-30:test_period]
        target_period, target_reds, target_blue = all_data[test_period]
        
        # 加载训练数据
        self.system.load_history(train_data)
        
        # 运行系统生成方案
        result = self.system.run_full_system(period_name=target_period)
        
        # 分析命中情况
        hit_analysis = self._analyze_hits(result, target_reds, target_blue)
        
        return {
            'period': target_period,
            'target_reds': target_reds,
            'target_blue': target_blue,
            'focus_pool': result['focus_pool'],
            'elite_core': result['elite_core'],
            'tickets': result['tickets'],
            'hit_analysis': hit_analysis,
            'total_cost': result['total_cost']
        }
    
    def _analyze_hits(self, result: Dict, target_reds: List[int], target_blue: int) -> Dict:
        """分析命中情况"""
        target_set = set(target_reds)
        
        analysis = {
            'focus_pool_hits': len(set(result['focus_pool']) & target_set),
            'elite_core_hits': len(set(result['elite_core']) & target_set),
            'engine_hits': {
                'A': {'max_reds': 0, 'blue_hit': False, 'tickets': []},
                'B': {'max_reds': 0, 'blue_hit': False, 'tickets': []},
                'C': {'max_reds': 0, 'blue_hit': False, 'tickets': []}
            },
            'best_ticket': None,
            'max_reds_hit': 0,
            'blue_hit': False
        }
        
        # 分析每张票
        max_reds = 0
        best_ticket = None
        
        for ticket in result['tickets']:
            engine = ticket['engine'].split('-')[0]
            reds_hit = len(set(ticket['reds']) & target_set)
            blue_hit = ticket['blue'] == target_blue
            
            # 更新引擎统计
            if reds_hit > analysis['engine_hits'][engine]['max_reds']:
                analysis['engine_hits'][engine]['max_reds'] = reds_hit
            if blue_hit:
                analysis['engine_hits'][engine]['blue_hit'] = True
            
            analysis['engine_hits'][engine]['tickets'].append({
                'reds_hit': reds_hit,
                'blue_hit': blue_hit
            })
            
            # 更新全局最佳
            if reds_hit > max_reds:
                max_reds = reds_hit
                best_ticket = ticket
            
            if blue_hit:
                analysis['blue_hit'] = True
        
        analysis['max_reds_hit'] = max_reds
        analysis['best_ticket'] = best_ticket
        
        return analysis
    
    def run_full_backtest(self, periods: int = 70) -> List[Dict]:
        """
        运行完整回测
        periods: 要回测的期数（需要前30期作为初始数据）
        """
        print(f"{'='*80}")
        print(f"V9.0系统历史回测 - 开始")
        print(f"{'='*80}\n")
        
        # 加载历史数据
        all_data = self.load_historical_data()
        total_periods = len(all_data)
        
        print(f"📊 数据加载完成：")
        print(f"   总期数：{total_periods}")
        print(f"   可回测期数：{total_periods - 30} (需要前30期作为训练)")
        print(f"   实际回测：{periods} 期\n")
        
        # 开始回测
        results = []
        
        for i in range(30, min(30 + periods, total_periods)):
            print(f"回测进度：{i-29}/{periods} - 期号 {all_data[i][0]}", end='\r')
            
            result = self.backtest_single_period(i, all_data)
            if result:
                results.append(result)
        
        print(f"\n\n✅ 回测完成！共回测 {len(results)} 期\n")
        
        self.results = results
        return results
    
    def generate_statistics_report(self) -> Dict:
        """生成统计分析报告"""
        if not self.results:
            return {}
        
        stats = {
            'total_periods': len(self.results),
            'total_cost': sum(r['total_cost'] for r in self.results),
            'focus_pool_coverage': {
                '6红': 0, '5红': 0, '4红': 0, '3红': 0, '2红': 0, '1红': 0, '0红': 0
            },
            'elite_core_coverage': {
                '6红': 0, '5红': 0, '4红': 0, '3红': 0, '2红': 0, '1红': 0, '0红': 0
            },
            'hit_distribution': {
                '6红': 0, '5红': 0, '4红': 0, '3红': 0, '2红': 0, '1红': 0, '0红': 0
            },
            'blue_hit_count': 0,
            'engine_performance': {
                'A': {'6红': 0, '5红': 0, '4红': 0, '3红': 0, '2红': 0, '1红': 0, '0红': 0},
                'B': {'6红': 0, '5红': 0, '4红': 0, '3红': 0, '2红': 0, '1红': 0, '0红': 0},
                'C': {'6红': 0, '5红': 0, '4红': 0, '3红': 0, '2红': 0, '1红': 0, '0红': 0},
            },
            'best_cases': []
        }
        
        # 统计数据
        for result in self.results:
            hit = result['hit_analysis']
            
            # 聚焦池覆盖
            focus_hits = hit['focus_pool_hits']
            stats['focus_pool_coverage'][f'{focus_hits}红'] += 1
            
            # 精华核心覆盖
            elite_hits = hit['elite_core_hits']
            stats['elite_core_coverage'][f'{elite_hits}红'] += 1
            
            # 最大命中分布
            max_reds = hit['max_reds_hit']
            stats['hit_distribution'][f'{max_reds}红'] += 1
            
            # 蓝球命中
            if hit['blue_hit']:
                stats['blue_hit_count'] += 1
            
            # 引擎性能
            for engine in ['A', 'B', 'C']:
                engine_max = hit['engine_hits'][engine]['max_reds']
                stats['engine_performance'][engine][f'{engine_max}红'] += 1
            
            # 记录5红以上的案例
            if max_reds >= 5:
                stats['best_cases'].append({
                    'period': result['period'],
                    'reds_hit': max_reds,
                    'blue_hit': hit['blue_hit'],
                    'focus_pool': result['focus_pool'],
                    'elite_core': result['elite_core'],
                    'target_reds': result['target_reds'],
                    'best_ticket': hit['best_ticket']
                })
        
        return stats
    
    def print_report(self, stats: Dict):
        """打印分析报告"""
        if not stats:
            print("⚠️  没有统计数据")
            return
        
        total = stats['total_periods']
        
        print(f"\n{'='*80}")
        print(f"V9.0系统回测分析报告")
        print(f"{'='*80}\n")
        
        # 基本信息
        print(f"📊 基本信息：")
        print(f"   回测期数：{total} 期")
        print(f"   总成本：{stats['total_cost']} 元")
        print(f"   单期平均：{stats['total_cost']/total:.1f} 元\n")
        
        # 聚焦池覆盖率
        print(f"🎯 动态聚焦池覆盖率（13码）：")
        for key in ['6红', '5红', '4红', '3红', '2红', '1红', '0红']:
            count = stats['focus_pool_coverage'][key]
            pct = count / total * 100
            bar = '█' * int(pct / 2)
            print(f"   {key}: {count:3d}期 ({pct:5.1f}%) {bar}")
        
        focus_4plus = sum(stats['focus_pool_coverage'][k] for k in ['6红', '5红', '4红'])
        print(f"   → 4红及以上：{focus_4plus}期 ({focus_4plus/total*100:.1f}%)\n")
        
        # 精华核心覆盖率
        print(f"💎 精华核心覆盖率（3-8码）：")
        for key in ['6红', '5红', '4红', '3红', '2红', '1红', '0红']:
            count = stats['elite_core_coverage'][key]
            pct = count / total * 100
            bar = '█' * int(pct / 2)
            print(f"   {key}: {count:3d}期 ({pct:5.1f}%) {bar}")
        
        elite_4plus = sum(stats['elite_core_coverage'][k] for k in ['6红', '5红', '4红'])
        print(f"   → 4红及以上：{elite_4plus}期 ({elite_4plus/total*100:.1f}%)\n")
        
        # 实际命中分布
        print(f"🎲 实际命中分布（最佳票）：")
        for key in ['6红', '5红', '4红', '3红', '2红', '1红', '0红']:
            count = stats['hit_distribution'][key]
            pct = count / total * 100
            bar = '█' * int(pct / 2)
            print(f"   {key}: {count:3d}期 ({pct:5.1f}%) {bar}")
        
        hit_4plus = sum(stats['hit_distribution'][k] for k in ['6红', '5红', '4红'])
        hit_5plus = sum(stats['hit_distribution'][k] for k in ['6红', '5红'])
        hit_6 = stats['hit_distribution']['6红']
        
        print(f"   → 4红及以上：{hit_4plus}期 ({hit_4plus/total*100:.1f}%)")
        print(f"   → 5红及以上：{hit_5plus}期 ({hit_5plus/total*100:.1f}%)")
        print(f"   → 6红：{hit_6}期 ({hit_6/total*100:.1f}%)\n")
        
        # 蓝球命中
        blue_pct = stats['blue_hit_count'] / total * 100
        print(f"🔵 蓝球命中：{stats['blue_hit_count']}期 ({blue_pct:.1f}%)\n")
        
        # 引擎性能对比
        print(f"⚙️  三引擎性能对比：\n")
        for engine, name in [('A', '精准层'), ('B', '稳健层'), ('C', '防御层')]:
            print(f"   引擎{engine} - {name}：")
            perf = stats['engine_performance'][engine]
            engine_4plus = sum(perf[k] for k in ['6红', '5红', '4红'])
            engine_5plus = sum(perf[k] for k in ['6红', '5红'])
            print(f"      4红+: {engine_4plus}期 ({engine_4plus/total*100:.1f}%)")
            print(f"      5红+: {engine_5plus}期 ({engine_5plus/total*100:.1f}%)")
            print(f"      6红:  {perf['6红']}期 ({perf['6红']/total*100:.1f}%)")
        
        print()
        
        # 最佳案例
        if stats['best_cases']:
            print(f"🏆 优秀案例（5红以上）：")
            for case in stats['best_cases'][:10]:  # 显示前10个
                blue_mark = "✓" if case['blue_hit'] else "✗"
                print(f"   期号 {case['period']}: {case['reds_hit']}红+{blue_mark}蓝")
                print(f"      目标: {', '.join([f'{r:02d}' for r in case['target_reds']])}")
                print(f"      聚焦池覆盖: {len(set(case['focus_pool']) & set(case['target_reds']))}红")
                print(f"      精华核心覆盖: {len(set(case['elite_core']) & set(case['target_reds']))}红")
                if case['best_ticket']:
                    print(f"      最佳票: {', '.join([f'{r:02d}' for r in case['best_ticket']['reds']])}")
                print()
        
        print(f"{'='*80}\n")
    
    def generate_optimization_suggestions(self, stats: Dict) -> List[str]:
        """生成优化建议"""
        if not stats:
            return []
        
        suggestions = []
        total = stats['total_periods']
        
        # 分析聚焦池表现
        focus_6 = stats['focus_pool_coverage']['6红']
        focus_5 = stats['focus_pool_coverage']['5红']
        focus_4 = stats['focus_pool_coverage']['4红']
        
        if focus_6 == 0:
            suggestions.append({
                'priority': 'HIGH',
                'issue': '聚焦池从未完全覆盖6红',
                'suggestion': '考虑扩大聚焦池到15-16码，或调整热冷权重算法'
            })
        
        if (focus_5 + focus_6) / total < 0.1:
            suggestions.append({
                'priority': 'HIGH',
                'issue': '聚焦池覆盖5红以上的概率过低',
                'suggestion': '需要优化断组规则，减少对黄金池号码的惩罚'
            })
        
        # 分析精华核心表现
        elite_6 = stats['elite_core_coverage']['6红']
        elite_5 = stats['elite_core_coverage']['5红']
        
        if elite_6 == 0 and elite_5 == 0:
            suggestions.append({
                'priority': 'HIGH',
                'issue': '精华核心从未覆盖5红以上',
                'suggestion': '29组交集算法可能过于保守，建议改用并集或加权选择'
            })
        
        # 分析实际命中
        hit_6 = stats['hit_distribution']['6红']
        hit_5 = stats['hit_distribution']['5红']
        hit_4 = stats['hit_distribution']['4红']
        
        if hit_6 == 0:
            suggestions.append({
                'priority': 'CRITICAL',
                'issue': f'{total}期回测中未命中6红',
                'suggestion': '当前方案难以命中6红，建议：1)增加总注数 2)优化号码选择算法 3)调整引擎配置'
            })
        
        if hit_5 / total < 0.05:
            suggestions.append({
                'priority': 'HIGH',
                'issue': '5红命中率过低',
                'suggestion': '聚焦池号码质量不足，需要改进热冷分析或增加其他维度（如AC值、和值等）'
            })
        
        # 分析引擎效率
        engine_a_best = sum(stats['engine_performance']['A'][k] for k in ['6红', '5红'])
        engine_b_best = sum(stats['engine_performance']['B'][k] for k in ['6红', '5红'])
        
        if engine_b_best > engine_a_best * 2:
            suggestions.append({
                'priority': 'MEDIUM',
                'issue': 'B引擎表现明显优于A引擎',
                'suggestion': '精华核心的筛选可能过于严格，建议放宽交集条件或增加核心码数'
            })
        
        if engine_a_best == 0:
            suggestions.append({
                'priority': 'HIGH',
                'issue': 'A引擎（精准层）从未命中高奖',
                'suggestion': 'A引擎策略需要重新设计，当前6-8码不足以保证高命中'
            })
        
        # 分析蓝球
        blue_hit_rate = stats['blue_hit_count'] / total
        if blue_hit_rate < 0.1:
            suggestions.append({
                'priority': 'MEDIUM',
                'issue': '蓝球命中率低于理论值',
                'suggestion': '双蓝策略可能需要调整，考虑增加到3-4个蓝球或改进冷热判断'
            })
        
        return suggestions
    
    def print_optimization_suggestions(self, suggestions: List[Dict]):
        """打印优化建议"""
        if not suggestions:
            print("✅ 系统表现良好，暂无明显优化空间\n")
            return
        
        print(f"{'='*80}")
        print(f"优化建议")
        print(f"{'='*80}\n")
        
        # 按优先级分组
        critical = [s for s in suggestions if s['priority'] == 'CRITICAL']
        high = [s for s in suggestions if s['priority'] == 'HIGH']
        medium = [s for s in suggestions if s['priority'] == 'MEDIUM']
        
        if critical:
            print(f"🔴 【紧急】需要立即优化：\n")
            for i, sug in enumerate(critical, 1):
                print(f"{i}. 问题：{sug['issue']}")
                print(f"   建议：{sug['suggestion']}\n")
        
        if high:
            print(f"🟠 【重要】建议优化：\n")
            for i, sug in enumerate(high, 1):
                print(f"{i}. 问题：{sug['issue']}")
                print(f"   建议：{sug['suggestion']}\n")
        
        if medium:
            print(f"🟡 【一般】可选优化：\n")
            for i, sug in enumerate(medium, 1):
                print(f"{i}. 问题：{sug['issue']}")
                print(f"   建议：{sug['suggestion']}\n")
        
        print(f"{'='*80}\n")


def main():
    """主函数"""
    print(f"\n{'#'*80}")
    print(f"# 双色球V9.0系统 - 历史回测验证")
    print(f"# 目标：评估命中率，优化6红捕获能力")
    print(f"# 执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*80}\n")
    
    # 创建分析器
    analyzer = V9BacktestAnalyzer()
    
    # 运行回测（回测70期）
    results = analyzer.run_full_backtest(periods=70)
    
    # 生成统计报告
    stats = analyzer.generate_statistics_report()
    
    # 打印报告
    analyzer.print_report(stats)
    
    # 生成优化建议
    suggestions = analyzer.generate_optimization_suggestions(stats)
    analyzer.print_optimization_suggestions(suggestions)
    
    # 保存结果
    output_file = 'V9系统回测结果.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'stats': stats,
            'suggestions': suggestions,
            'summary': {
                '回测期数': stats['total_periods'],
                '6红命中': stats['hit_distribution']['6红'],
                '5红命中': stats['hit_distribution']['5红'],
                '4红命中': stats['hit_distribution']['4红'],
                '总成本': stats['total_cost']
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"💾 回测结果已保存到：{output_file}\n")
    
    print(f"{'='*80}")
    print(f"回测完成！")
    print(f"{'='*80}\n")
    
    return stats, suggestions


if __name__ == "__main__":
    stats, suggestions = main()
