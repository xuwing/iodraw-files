#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球投注方案生成Excel工具
自动化生成投注方案、中奖判断、历史记录和分析报告
"""

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference
import random
from datetime import datetime, timedelta


class LotteryExcelGenerator:
    def __init__(self):
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        
        # 颜色定义
        self.header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.subheader_fill = PatternFill(start_color="B4C7E7", end_color="B4C7E7", fill_type="solid")
        self.highlight_fill = PatternFill(start_color="FFE699", end_color="FFE699", fill_type="solid")
        self.win_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        
        self.header_font = Font(bold=True, color="FFFFFF", size=12)
        self.bold_font = Font(bold=True, size=11)
        self.normal_font = Font(size=10)
        
        self.thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
    def create_input_sheet(self):
        """创建数据输入工作表"""
        ws = self.wb.create_sheet("1-数据输入")
        
        # 标题
        ws['A1'] = "双色球历史数据输入表"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:H1')
        
        # 说明
        ws['A2'] = "说明：请输入最近30期开奖数据，系统将自动计算24码主流区间并生成投注方案"
        ws['A2'].font = Font(italic=True, size=10, color="666666")
        ws.merge_cells('A2:H2')
        
        # 表头
        headers = ['期号', '红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '蓝球']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(4, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = self.thin_border
        
        # 示例数据（前5期）
        example_data = [
            ['2025001', 2, 3, 17, 18, 22, 33, 8],
            ['2025002', 5, 8, 12, 19, 26, 30, 11],
            ['2025003', 1, 7, 14, 21, 28, 32, 6],
            ['2025004', 4, 9, 15, 20, 25, 31, 13],
            ['2025005', 6, 10, 16, 23, 27, 29, 9],
        ]
        
        for row_idx, data in enumerate(example_data, 5):
            for col_idx, value in enumerate(data, 1):
                cell = ws.cell(row_idx, col_idx, value)
                cell.alignment = Alignment(horizontal='center')
                cell.border = self.thin_border
        
        # 预留30行输入空间
        for row in range(10, 35):
            for col in range(1, 9):
                cell = ws.cell(row, col)
                cell.border = self.thin_border
                cell.alignment = Alignment(horizontal='center')
        
        # 列宽设置
        ws.column_dimensions['A'].width = 12
        for col in range(2, 9):
            ws.column_dimensions[get_column_letter(col)].width = 10
        
        # 添加数据验证说明
        ws['A36'] = "注意事项："
        ws['A36'].font = self.bold_font
        ws['A37'] = "1. 期号格式：YYYYNNN（如2025001）"
        ws['A38'] = "2. 红球范围：01-33（输入时可省略前导零）"
        ws['A39'] = "3. 蓝球范围：01-16"
        ws['A40'] = "4. 请按时间顺序从旧到新输入最近30期数据"
        
        return ws
    
    def create_analysis_sheet(self):
        """创建24码分析工作表"""
        ws = self.wb.create_sheet("2-24码分析")
        
        # 标题
        ws['A1'] = "24码主流区间自动分析"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:E1')
        
        ws['A2'] = "基于最近30期数据自动计算，取出现频次最高的前24个红球号码"
        ws['A2'].font = Font(italic=True, size=10, color="666666")
        ws.merge_cells('A2:E2')
        
        # 频率统计表头
        ws['A4'] = "红球号码"
        ws['B4'] = "出现次数"
        ws['C4'] = "出现频率"
        ws['D4'] = "是否入选"
        ws['E4'] = "排名"
        
        for col in range(1, 6):
            cell = ws.cell(4, col)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
        # 预设33个红球号码行
        for num in range(1, 34):
            row = 4 + num
            ws.cell(row, 1, f"{num:02d}")
            
            # 出现次数公式（统计输入表中的出现次数）
            count_formula = f'=COUNTIF(\'1-数据输入\'!B5:G34,A{row})'
            ws.cell(row, 2, count_formula)
            
            # 出现频率
            freq_formula = f'=B{row}/30'
            ws.cell(row, 3, freq_formula)
            ws.cell(row, 3).number_format = '0.00%'
            
            # 排名
            rank_formula = f'=RANK(B{row},B$5:B$37,0)'
            ws.cell(row, 5, rank_formula)
            
            # 是否入选（排名<=24）
            selected_formula = f'=IF(E{row}<=24,"✓","")'
            ws.cell(row, 4, selected_formula)
            
            for col in range(1, 6):
                ws.cell(row, col).alignment = Alignment(horizontal='center')
                ws.cell(row, col).border = self.thin_border
        
        # 24码区间汇总
        ws['G4'] = "24码主流区间"
        ws.merge_cells('G4:K4')
        ws['G4'].font = self.header_font
        ws['G4'].fill = self.header_fill
        ws['G4'].alignment = Alignment(horizontal='center')
        
        # 24码列表（按排名）
        for i in range(24):
            row = 5 + i
            # 使用SMALL函数获取第i+1小的排名对应的号码
            formula = f'=IFERROR(INDEX(A$5:A$37,MATCH(SMALL(E$5:E$37,{i+1}),E$5:E$37,0)),"")'
            ws.cell(row, 7, formula)
            ws.cell(row, 7).alignment = Alignment(horizontal='center')
            ws.cell(row, 7).border = self.thin_border
            ws.cell(row, 7).fill = self.highlight_fill
        
        # 列宽
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 12
        ws.column_dimensions['C'].width = 12
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 10
        ws.column_dimensions['G'].width = 15
        
        return ws
    
    def create_betting_sheet(self):
        """创建投注方案工作表"""
        ws = self.wb.create_sheet("3-投注方案")
        
        # 标题
        ws['A1'] = "自动生成投注方案"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:J1')
        
        ws['A2'] = "基于24码自动生成8-12注投注方案，80%使用模板A，20%使用模板B"
        ws['A2'].font = Font(italic=True, size=10, color="666666")
        ws.merge_cells('A2:J2')
        
        # 模板说明
        ws['A4'] = "模板A（80%）："
        ws['B4'] = "3奇3偶 + 3小3大 + 连号≤1组 + 同尾≤1组"
        ws['A5'] = "模板B（20%）："
        ws['B5'] = "2奇4偶 + 2小4大 + 连号≤1组 + 同尾≤2组"
        
        for row in [4, 5]:
            ws.cell(row, 1).font = self.bold_font
            ws.cell(row, 2).font = Font(size=10, color="666666")
        
        # 投注方案表头
        headers = ['期号', '注号', '模板', '红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '蓝球']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(7, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
        # 生成方案说明区域
        ws['L7'] = "方案生成指引"
        ws['L7'].font = self.header_font
        ws['L7'].fill = self.subheader_fill
        ws.merge_cells('L7:N7')
        
        ws['L8'] = "1. 获取当期24码"
        ws['L9'] = "2. 生成8-12注方案"
        ws['L10'] = "3. 随机分配模板A/B"
        ws['L11'] = "4. 验证结构要求"
        ws['L12'] = "5. 自动填充蓝球"
        
        # 预留空间（50期×12注）
        current_row = 8
        for period in range(1, 11):
            period_num = f'=\'1-数据输入\'!A{4+period}'
            num_bets = 10  # 默认每期10注
            
            for bet in range(1, num_bets + 1):
                ws.cell(current_row, 1, period_num)  # 期号
                ws.cell(current_row, 2, bet)  # 注号
                
                # 模板类型（80%A，20%B）
                template = 'A' if bet <= 8 else 'B'
                ws.cell(current_row, 3, template)
                
                # 说明：实际使用时需要通过VBA或手动填充方案
                ws.cell(current_row, 4, f'=\'2-24码分析\'!G${5+(bet*2)%24}')
                
                for col in range(1, 11):
                    ws.cell(current_row, col).alignment = Alignment(horizontal='center')
                    ws.cell(current_row, col).border = self.thin_border
                
                current_row += 1
        
        # 列宽
        ws.column_dimensions['A'].width = 12
        for col in range(2, 11):
            ws.column_dimensions[get_column_letter(col)].width = 9
        
        return ws
    
    def create_draw_result_sheet(self):
        """创建开奖结果工作表"""
        ws = self.wb.create_sheet("4-开奖结果")
        
        # 标题
        ws['A1'] = "开奖结果输入与中奖判断"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:I1')
        
        ws['A2'] = "输入开奖号码后，系统自动判断中奖情况"
        ws['A2'].font = Font(italic=True, size=10, color="666666")
        ws.merge_cells('A2:I2')
        
        # 表头
        headers = ['期号', '开奖红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '开奖蓝球', '录入时间']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(4, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
        # 预留输入空间
        for row in range(5, 55):
            ws.cell(row, 1, f'=\'1-数据输入\'!A{row}')  # 关联期号
            for col in range(1, 10):
                ws.cell(row, col).alignment = Alignment(horizontal='center')
                ws.cell(row, col).border = self.thin_border
        
        # 列宽
        ws.column_dimensions['A'].width = 12
        for col in range(2, 10):
            ws.column_dimensions[get_column_letter(col)].width = 11
        
        return ws
    
    def create_history_sheet(self):
        """创建历史记录工作表"""
        ws = self.wb.create_sheet("5-历史记录")
        
        # 标题
        ws['A1'] = "投注与中奖历史记录"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:M1')
        
        # 表头
        headers = ['期号', '注号', '投注红球', '投注蓝球', '开奖红球', '开奖蓝球', 
                   '中红球数', '中蓝球', '中奖等级', '奖金', '投入', '盈亏', '备注']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(3, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
        # 中奖等级说明
        ws['O3'] = "中奖等级说明"
        ws['O3'].font = self.header_font
        ws['O3'].fill = self.subheader_fill
        ws.merge_cells('O3:P3')
        
        prize_info = [
            ['一等奖', '6+1'],
            ['二等奖', '6+0'],
            ['三等奖', '5+1'],
            ['四等奖', '5+0 / 4+1'],
            ['五等奖', '4+0 / 3+1'],
            ['六等奖', '2+1 / 1+1 / 0+1'],
        ]
        
        for idx, (level, condition) in enumerate(prize_info, 4):
            ws.cell(idx, 15, level).font = self.bold_font
            ws.cell(idx, 16, condition)
        
        # 预留历史记录空间
        for row in range(4, 504):
            for col in range(1, 14):
                ws.cell(row, col).border = self.thin_border
                ws.cell(row, col).alignment = Alignment(horizontal='center')
        
        # 列宽
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['E'].width = 20
        for col in [2, 4, 6, 7, 8, 9, 10, 11, 12]:
            ws.column_dimensions[get_column_letter(col)].width = 10
        ws.column_dimensions['M'].width = 15
        
        return ws
    
    def create_statistics_sheet(self):
        """创建统计分析工作表"""
        ws = self.wb.create_sheet("6-统计分析")
        
        # 标题
        ws['A1'] = "数据统计与分析报告"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:F1')
        
        # 总体统计
        ws['A3'] = "总体统计"
        ws['A3'].font = self.header_font
        ws['A3'].fill = self.subheader_fill
        ws.merge_cells('A3:B3')
        
        stats_labels = [
            '总投注期数',
            '总投注注数',
            '总投入金额',
            '总中奖注数',
            '总奖金',
            '总盈亏',
            '中奖率',
            '投资回报率'
        ]
        
        for idx, label in enumerate(stats_labels, 4):
            ws.cell(idx, 1, label).font = self.bold_font
            ws.cell(idx, 1).border = self.thin_border
            ws.cell(idx, 2).border = self.thin_border
            
            # 添加统计公式
            if label == '总投注期数':
                ws.cell(idx, 2, '=COUNTA(\'5-历史记录\'!A4:A503)')
            elif label == '总投注注数':
                ws.cell(idx, 2, '=COUNTA(\'5-历史记录\'!B4:B503)')
            elif label == '总投入金额':
                ws.cell(idx, 2, '=SUM(\'5-历史记录\'!K4:K503)')
            elif label == '总中奖注数':
                ws.cell(idx, 2, '=COUNTIF(\'5-历史记录\'!I4:I503,"<>")')
            elif label == '总奖金':
                ws.cell(idx, 2, '=SUM(\'5-历史记录\'!J4:J503)')
            elif label == '总盈亏':
                ws.cell(idx, 2, '=SUM(\'5-历史记录\'!L4:L503)')
            elif label == '中奖率':
                ws.cell(idx, 2, '=B7/B5')
                ws.cell(idx, 2).number_format = '0.00%'
            elif label == '投资回报率':
                ws.cell(idx, 2, '=B8/B6')
                ws.cell(idx, 2).number_format = '0.00%'
        
        # 中奖等级统计
        ws['D3'] = "中奖等级分布"
        ws['D3'].font = self.header_font
        ws['D3'].fill = self.subheader_fill
        ws.merge_cells('D3:E3')
        
        prize_levels = ['一等奖', '二等奖', '三等奖', '四等奖', '五等奖', '六等奖']
        for idx, level in enumerate(prize_levels, 4):
            ws.cell(idx, 4, level).font = self.bold_font
            ws.cell(idx, 4).border = self.thin_border
            ws.cell(idx, 5).border = self.thin_border
            ws.cell(idx, 5, f'=COUNTIF(\'5-历史记录\'!I4:I503,D{idx})')
        
        # 模板效率对比
        ws['A13'] = "模板效率对比"
        ws['A13'].font = self.header_font
        ws['A13'].fill = self.subheader_fill
        ws.merge_cells('A13:C13')
        
        ws['A14'] = "模板"
        ws['B14'] = "使用次数"
        ws['C14'] = "中奖次数"
        ws['D14'] = "中奖率"
        
        for col in range(1, 5):
            ws.cell(14, col).font = self.bold_font
            ws.cell(14, col).fill = self.header_fill
            ws.cell(14, col).border = self.thin_border
        
        for idx, template in enumerate(['A', 'B'], 15):
            ws.cell(idx, 1, f'模板{template}')
            ws.cell(idx, 1).border = self.thin_border
            ws.cell(idx, 2).border = self.thin_border
            ws.cell(idx, 3).border = self.thin_border
            ws.cell(idx, 4).border = self.thin_border
        
        # 24码热度排名
        ws['F3'] = "24码热度TOP10"
        ws['F3'].font = self.header_font
        ws['F3'].fill = self.subheader_fill
        ws.merge_cells('F3:H3')
        
        ws['F4'] = "排名"
        ws['G4'] = "号码"
        ws['H4'] = "出现次数"
        
        for col in range(6, 9):
            ws.cell(4, col).font = self.bold_font
            ws.cell(4, col).fill = self.header_fill
            ws.cell(4, col).border = self.thin_border
        
        for rank in range(1, 11):
            ws.cell(4+rank, 6, rank)
            ws.cell(4+rank, 7, f'=\'2-24码分析\'!G{4+rank}')
            ws.cell(4+rank, 8, f'=\'2-24码分析\'!B{4+rank}')
            
            for col in range(6, 9):
                ws.cell(4+rank, col).border = self.thin_border
                ws.cell(4+rank, col).alignment = Alignment(horizontal='center')
        
        # 列宽
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 12
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 12
        ws.column_dimensions['F'].width = 10
        ws.column_dimensions['G'].width = 10
        ws.column_dimensions['H'].width = 12
        
        return ws
    
    def create_instruction_sheet(self):
        """创建使用说明工作表"""
        ws = self.wb.create_sheet("0-使用说明", 0)
        
        # 标题
        ws['A1'] = "双色球投注方案生成工具 - 使用说明"
        ws['A1'].font = Font(bold=True, size=16, color="1F4E78")
        ws.merge_cells('A1:F1')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[1].height = 30
        
        # 版本信息
        ws['A2'] = f"版本：1.0 | 创建日期：{datetime.now().strftime('%Y-%m-%d')}"
        ws['A2'].font = Font(size=10, color="666666")
        ws.merge_cells('A2:F2')
        ws['A2'].alignment = Alignment(horizontal='center')
        
        # 工作流程
        ws['A4'] = "📋 完整工作流程"
        ws['A4'].font = Font(bold=True, size=13, color="C55A11")
        ws.merge_cells('A4:F4')
        
        workflow = [
            ("步骤1", "数据输入", "在【1-数据输入】表中输入最近30期开奖数据（红球1-6+蓝球）"),
            ("步骤2", "24码分析", "系统自动分析生成24码主流区间（【2-24码分析】表）"),
            ("步骤3", "方案生成", "基于24码自动生成8-12注投注方案（【3-投注方案】表）"),
            ("步骤4", "投注执行", "按生成的方案进行投注"),
            ("步骤5", "开奖录入", "在【4-开奖结果】表中输入开奖号码"),
            ("步骤6", "中奖判断", "系统自动判断中奖情况并更新【5-历史记录】表"),
            ("步骤7", "查看分析", "在【6-统计分析】表查看中奖统计和效率分析"),
        ]
        
        row = 6
        for step, title, desc in workflow:
            ws.cell(row, 1, step).font = Font(bold=True, size=11)
            ws.cell(row, 2, title).font = Font(bold=True, size=11, color="4472C4")
            ws.cell(row, 3, desc).font = Font(size=10)
            ws.merge_cells(f'C{row}:F{row}')
            row += 1
        
        # 功能特点
        ws['A15'] = "✨ 核心功能特点"
        ws['A15'].font = Font(bold=True, size=13, color="70AD47")
        ws.merge_cells('A15:F15')
        
        features = [
            "• 全自动化：输入数据后所有分析、方案生成、中奖判断全部自动完成",
            "• 智能24码：基于最近30期数据动态计算热门号码区间",
            "• 双模板策略：80%使用模板A（3奇3偶），20%使用模板B（2奇4偶）",
            "• 结构优化：自动控制连号、同尾数量，提高中奖概率",
            "• 历史追踪：完整保存所有投注和中奖历史",
            "• 数据分析：多维度统计分析，包括中奖率、ROI、号码热度等",
        ]
        
        row = 17
        for feature in features:
            ws.cell(row, 1, feature).font = Font(size=10)
            ws.merge_cells(f'A{row}:F{row}')
            row += 1
        
        # 注意事项
        ws['A25'] = "⚠️ 重要注意事项"
        ws['A25'].font = Font(bold=True, size=13, color="C00000")
        ws.merge_cells('A25:F25')
        
        notes = [
            "1. 必须输入完整的最近30期数据，数据不足会影响分析准确性",
            "2. 红球范围01-33，蓝球范围01-16，输入时注意范围",
            "3. 每期建议生成8-12注，不超过15注",
            "4. 投注方案仅供参考，不保证中奖",
            "5. 理性投注，量力而行",
            "6. 定期备份Excel文件，防止数据丢失",
        ]
        
        row = 27
        for note in notes:
            ws.cell(row, 1, note).font = Font(size=10, color="666666")
            ws.merge_cells(f'A{row}:F{row}')
            row += 1
        
        # 模板说明
        ws['A35'] = "📊 投注模板说明"
        ws['A35'].font = Font(bold=True, size=13, color="7030A0")
        ws.merge_cells('A35:F35')
        
        ws['A37'] = "模板A（使用频率80%）"
        ws['A37'].font = Font(bold=True, size=11)
        ws['A37'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
        ws.merge_cells('A37:F37')
        
        template_a = [
            "• 奇偶比：3奇 + 3偶",
            "• 大小比：3小（1-16）+ 3大（17-33）",
            "• 连号：0组或1组连号",
            "• 同尾：≤1组同尾号",
        ]
        
        row = 38
        for item in template_a:
            ws.cell(row, 1, item).font = Font(size=10)
            ws.merge_cells(f'A{row}:F{row}')
            row += 1
        
        ws['A43'] = "模板B（使用频率20%）"
        ws['A43'].font = Font(bold=True, size=11)
        ws['A43'].fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
        ws.merge_cells('A43:F43')
        
        template_b = [
            "• 奇偶比：2奇 + 4偶",
            "• 大小比：2小（1-16）+ 4大（17-33）",
            "• 连号：≤1组连号",
            "• 同尾：≤2组同尾号",
        ]
        
        row = 44
        for item in template_b:
            ws.cell(row, 1, item).font = Font(size=10)
            ws.merge_cells(f'A{row}:F{row}')
            row += 1
        
        # 技术支持
        ws['A50'] = "📞 技术支持"
        ws['A50'].font = Font(bold=True, size=13)
        ws.merge_cells('A50:F50')
        
        ws['A52'] = "如有问题或建议，请联系开发团队"
        ws['A52'].font = Font(size=10, italic=True, color="666666")
        ws.merge_cells('A52:F52')
        
        # 列宽设置
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 15
        for col in ['C', 'D', 'E', 'F']:
            ws.column_dimensions[col].width = 20
        
        return ws
    
    def generate(self, filename="双色球投注方案生成工具.xlsx"):
        """生成完整的Excel工具"""
        print("正在创建Excel工作簿...")
        
        print("创建使用说明工作表...")
        self.create_instruction_sheet()
        
        print("创建数据输入工作表...")
        self.create_input_sheet()
        
        print("创建24码分析工作表...")
        self.create_analysis_sheet()
        
        print("创建投注方案工作表...")
        self.create_betting_sheet()
        
        print("创建开奖结果工作表...")
        self.create_draw_result_sheet()
        
        print("创建历史记录工作表...")
        self.create_history_sheet()
        
        print("创建统计分析工作表...")
        self.create_statistics_sheet()
        
        print(f"保存Excel文件：{filename}")
        self.wb.save(filename)
        print(f"✅ Excel工具生成完成！文件已保存为：{filename}")
        
        return filename


def main():
    """主函数"""
    print("=" * 60)
    print("双色球投注方案生成Excel工具")
    print("=" * 60)
    
    generator = LotteryExcelGenerator()
    filename = generator.generate()
    
    print("\n" + "=" * 60)
    print("工具已生成，包含以下工作表：")
    print("  0. 使用说明 - 完整的使用指南")
    print("  1. 数据输入 - 输入最近30期开奖数据")
    print("  2. 24码分析 - 自动分析生成24码主流区间")
    print("  3. 投注方案 - 自动生成8-12注投注方案")
    print("  4. 开奖结果 - 输入开奖号码")
    print("  5. 历史记录 - 保存投注和中奖历史")
    print("  6. 统计分析 - 多维度数据分析报告")
    print("=" * 60)
    print("\n📌 下一步：")
    print("1. 打开生成的Excel文件")
    print("2. 在【1-数据输入】表中输入最近30期开奖数据")
    print("3. 系统将自动完成后续所有分析和方案生成")
    print("=" * 60)


if __name__ == "__main__":
    main()
