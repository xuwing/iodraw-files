#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球投注方案生成Excel工具（增强版 - 含VBA自动化）
包含完整的VBA代码实现自动方案生成和中奖判断
"""

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime


class LotteryExcelGeneratorVBA:
    def __init__(self):
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        
        # 颜色定义
        self.header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.subheader_fill = PatternFill(start_color="B4C7E7", end_color="B4C7E7", fill_type="solid")
        self.highlight_fill = PatternFill(start_color="FFE699", end_color="FFE699", fill_type="solid")
        self.win_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        self.blue_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")
        
        self.header_font = Font(bold=True, color="FFFFFF", size=12)
        self.bold_font = Font(bold=True, size=11)
        self.normal_font = Font(size=10)
        
        self.thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def get_vba_code(self):
        """返回VBA代码"""
        return '''
' ========================================
' 双色球投注方案自动生成VBA代码
' ========================================

Option Explicit

' 主流程：生成投注方案
Sub 生成投注方案()
    Dim ws输入 As Worksheet, ws24码 As Worksheet, ws方案 As Worksheet
    Dim codes24() As Integer
    Dim i As Long, j As Long
    Dim lastRow As Long, startRow As Long
    Dim numBets As Integer
    Dim periodNum As String
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    Set ws输入 = ThisWorkbook.Worksheets("1-数据输入")
    Set ws24码 = ThisWorkbook.Worksheets("2-24码分析")
    Set ws方案 = ThisWorkbook.Worksheets("3-投注方案")
    
    ' 获取24码
    ReDim codes24(1 To 24)
    For i = 1 To 24
        If IsNumeric(ws24码.Cells(4 + i, 7).Value) Then
            codes24(i) = CInt(ws24码.Cells(4 + i, 7).Value)
        Else
            Exit For
        End If
    Next i
    
    If i <= 24 Then
        MsgBox "请先在【1-数据输入】表中输入完整的30期数据！", vbExclamation
        Application.ScreenUpdating = True
        Application.Calculation = xlCalculationAutomatic
        Exit Sub
    End If
    
    ' 清除旧方案
    lastRow = ws方案.Cells(ws方案.Rows.Count, 1).End(xlUp).Row
    If lastRow > 7 Then
        ws方案.Range("A8:J" & lastRow).ClearContents
    End If
    
    ' 生成方案
    startRow = 8
    For i = 5 To 34  ' 最多30期
        periodNum = ws输入.Cells(i, 1).Value
        If periodNum = "" Then Exit For
        
        ' 每期生成10注（8注模板A + 2注模板B）
        numBets = 10
        
        For j = 1 To numBets
            ws方案.Cells(startRow, 1).Value = periodNum  ' 期号
            ws方案.Cells(startRow, 2).Value = j  ' 注号
            
            ' 模板类型
            If j <= 8 Then
                ws方案.Cells(startRow, 3).Value = "A"
                Call Generate6Numbers(codes24, ws方案, startRow, "A")
            Else
                ws方案.Cells(startRow, 3).Value = "B"
                Call Generate6Numbers(codes24, ws方案, startRow, "B")
            End If
            
            ' 蓝球（1-16随机）
            ws方案.Cells(startRow, 10).Value = Int(Rnd() * 16) + 1
            
            startRow = startRow + 1
        Next j
    Next i
    
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    
    MsgBox "投注方案生成完成！共生成 " & (startRow - 8) & " 注", vbInformation
End Sub

' 生成6个红球号码
Sub Generate6Numbers(codes24() As Integer, ws As Worksheet, row As Long, template As String)
    Dim selected(1 To 6) As Integer
    Dim i As Integer, j As Integer, attempt As Integer
    Dim valid As Boolean
    Dim tempList() As Integer
    Dim n As Integer
    
    ReDim tempList(1 To 24)
    For i = 1 To 24
        tempList(i) = codes24(i)
    Next i
    
    ' 最多尝试100次
    For attempt = 1 To 100
        ' 洗牌
        For i = 1 To 24
            j = Int(Rnd() * 24) + 1
            n = tempList(i)
            tempList(i) = tempList(j)
            tempList(j) = n
        Next i
        
        ' 取前6个
        For i = 1 To 6
            selected(i) = tempList(i)
        Next i
        
        ' 排序
        Call BubbleSort(selected)
        
        ' 验证
        If ValidateNumbers(selected, template) Then
            valid = True
            Exit For
        End If
    Next attempt
    
    ' 如果验证失败，使用简单规则
    If Not valid Then
        For i = 1 To 6
            selected(i) = codes24(i)
        Next i
        Call BubbleSort(selected)
    End If
    
    ' 填充到工作表
    For i = 1 To 6
        ws.Cells(row, 3 + i).Value = selected(i)
    Next i
End Sub

' 冒泡排序
Sub BubbleSort(arr() As Integer)
    Dim i As Integer, j As Integer, temp As Integer
    For i = 1 To 5
        For j = i + 1 To 6
            If arr(i) > arr(j) Then
                temp = arr(i)
                arr(i) = arr(j)
                arr(j) = temp
            End If
        Next j
    Next i
End Sub

' 验证号码是否符合模板要求
Function ValidateNumbers(nums() As Integer, template As String) As Boolean
    Dim oddCount As Integer, evenCount As Integer
    Dim smallCount As Integer, largeCount As Integer
    Dim consecutiveCount As Integer, sameTailCount As Integer
    Dim i As Integer
    
    ' 统计奇偶
    For i = 1 To 6
        If nums(i) Mod 2 = 1 Then
            oddCount = oddCount + 1
        Else
            evenCount = evenCount + 1
        End If
    Next i
    
    ' 统计大小
    For i = 1 To 6
        If nums(i) <= 16 Then
            smallCount = smallCount + 1
        Else
            largeCount = largeCount + 1
        End If
    Next i
    
    ' 统计连号
    consecutiveCount = 0
    For i = 1 To 5
        If nums(i + 1) - nums(i) = 1 Then
            consecutiveCount = consecutiveCount + 1
        End If
    Next i
    
    ' 统计同尾
    sameTailCount = 0
    For i = 1 To 5
        Dim j As Integer
        For j = i + 1 To 6
            If nums(i) Mod 10 = nums(j) Mod 10 Then
                sameTailCount = sameTailCount + 1
            End If
        Next j
    Next i
    
    ' 验证规则
    If template = "A" Then
        ' 模板A：3奇3偶，3小3大，连号≤1，同尾≤1
        If oddCount = 3 And evenCount = 3 And _
           smallCount = 3 And largeCount = 3 And _
           consecutiveCount <= 1 And sameTailCount <= 1 Then
            ValidateNumbers = True
        Else
            ValidateNumbers = False
        End If
    ElseIf template = "B" Then
        ' 模板B：2奇4偶，2小4大，连号≤1，同尾≤2
        If oddCount = 2 And evenCount = 4 And _
           smallCount = 2 And largeCount = 4 And _
           consecutiveCount <= 1 And sameTailCount <= 2 Then
            ValidateNumbers = True
        Else
            ValidateNumbers = False
        End If
    Else
        ValidateNumbers = False
    End If
End Function

' 中奖判断
Sub 判断中奖()
    Dim ws方案 As Worksheet, ws开奖 As Worksheet, ws历史 As Worksheet
    Dim i As Long, j As Long
    Dim periodNum As String, drawPeriod As String
    Dim betReds() As Integer, drawReds() As Integer
    Dim betBlue As Integer, drawBlue As Integer
    Dim matchRed As Integer, matchBlue As Boolean
    Dim prizeLevel As String
    Dim lastHistoryRow As Long
    
    Application.ScreenUpdating = False
    
    Set ws方案 = ThisWorkbook.Worksheets("3-投注方案")
    Set ws开奖 = ThisWorkbook.Worksheets("4-开奖结果")
    Set ws历史 = ThisWorkbook.Worksheets("5-历史记录")
    
    ' 获取历史记录最后一行
    lastHistoryRow = ws历史.Cells(ws历史.Rows.Count, 1).End(xlUp).Row + 1
    If lastHistoryRow < 4 Then lastHistoryRow = 4
    
    ' 遍历投注方案
    For i = 8 To 500
        periodNum = ws方案.Cells(i, 1).Value
        If periodNum = "" Then Exit For
        
        ' 查找对应的开奖结果
        drawPeriod = ""
        For j = 5 To 54
            If ws开奖.Cells(j, 1).Value = periodNum And _
               ws开奖.Cells(j, 2).Value <> "" Then
                drawPeriod = periodNum
                
                ' 获取开奖号码
                ReDim drawReds(1 To 6)
                For k = 1 To 6
                    drawReds(k) = ws开奖.Cells(j, 1 + k).Value
                Next k
                drawBlue = ws开奖.Cells(j, 8).Value
                
                Exit For
            End If
        Next j
        
        If drawPeriod <> "" Then
            ' 获取投注号码
            ReDim betReds(1 To 6)
            For k = 1 To 6
                betReds(k) = ws方案.Cells(i, 3 + k).Value
            Next k
            betBlue = ws方案.Cells(i, 10).Value
            
            ' 计算匹配数
            matchRed = CountMatches(betReds, drawReds)
            matchBlue = (betBlue = drawBlue)
            
            ' 判断中奖等级
            prizeLevel = GetPrizeLevel(matchRed, matchBlue)
            
            ' 记录到历史
            If prizeLevel <> "" Then
                ws历史.Cells(lastHistoryRow, 1).Value = periodNum
                ws历史.Cells(lastHistoryRow, 2).Value = ws方案.Cells(i, 2).Value
                ws历史.Cells(lastHistoryRow, 3).Value = Join_Array(betReds)
                ws历史.Cells(lastHistoryRow, 4).Value = betBlue
                ws历史.Cells(lastHistoryRow, 5).Value = Join_Array(drawReds)
                ws历史.Cells(lastHistoryRow, 6).Value = drawBlue
                ws历史.Cells(lastHistoryRow, 7).Value = matchRed
                ws历史.Cells(lastHistoryRow, 8).Value = IIf(matchBlue, "✓", "")
                ws历史.Cells(lastHistoryRow, 9).Value = prizeLevel
                ws历史.Cells(lastHistoryRow, 10).Value = GetPrizeMoney(prizeLevel)
                ws历史.Cells(lastHistoryRow, 11).Value = 2  ' 投入2元
                ws历史.Cells(lastHistoryRow, 12).Value = _
                    ws历史.Cells(lastHistoryRow, 10).Value - 2
                
                lastHistoryRow = lastHistoryRow + 1
            End If
        End If
    Next i
    
    Application.ScreenUpdating = True
    MsgBox "中奖判断完成！", vbInformation
End Sub

' 计算红球匹配数
Function CountMatches(bet() As Integer, draw() As Integer) As Integer
    Dim count As Integer, i As Integer, j As Integer
    count = 0
    For i = 1 To 6
        For j = 1 To 6
            If bet(i) = draw(j) Then
                count = count + 1
                Exit For
            End If
        Next j
    Next i
    CountMatches = count
End Function

' 判断中奖等级
Function GetPrizeLevel(redMatch As Integer, blueMatch As Boolean) As String
    If redMatch = 6 And blueMatch Then
        GetPrizeLevel = "一等奖"
    ElseIf redMatch = 6 And Not blueMatch Then
        GetPrizeLevel = "二等奖"
    ElseIf redMatch = 5 And blueMatch Then
        GetPrizeLevel = "三等奖"
    ElseIf (redMatch = 5 And Not blueMatch) Or (redMatch = 4 And blueMatch) Then
        GetPrizeLevel = "四等奖"
    ElseIf (redMatch = 4 And Not blueMatch) Or (redMatch = 3 And blueMatch) Then
        GetPrizeLevel = "五等奖"
    ElseIf (redMatch = 2 And blueMatch) Or (redMatch = 1 And blueMatch) Or (redMatch = 0 And blueMatch) Then
        GetPrizeLevel = "六等奖"
    Else
        GetPrizeLevel = ""
    End If
End Function

' 获取奖金金额（示例金额）
Function GetPrizeMoney(level As String) As Long
    Select Case level
        Case "一等奖"
            GetPrizeMoney = 5000000
        Case "二等奖"
            GetPrizeMoney = 200000
        Case "三等奖"
            GetPrizeMoney = 3000
        Case "四等奖"
            GetPrizeMoney = 200
        Case "五等奖"
            GetPrizeMoney = 10
        Case "六等奖"
            GetPrizeMoney = 5
        Case Else
            GetPrizeMoney = 0
    End Select
End Function

' 数组转字符串
Function Join_Array(arr() As Integer) As String
    Dim result As String, i As Integer
    result = Format(arr(1), "00")
    For i = 2 To 6
        result = result & "," & Format(arr(i), "00")
    Next i
    Join_Array = result
End Function

' 初始化随机数种子
Sub Auto_Open()
    Randomize
End Sub
'''
    
    def create_instruction_sheet_vba(self):
        """创建使用说明（VBA版本）"""
        ws = self.wb.create_sheet("0-使用说明", 0)
        
        # 标题
        ws['A1'] = "双色球投注方案生成工具（VBA自动化版）- 使用说明"
        ws['A1'].font = Font(bold=True, size=16, color="1F4E78")
        ws.merge_cells('A1:G1')
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws.row_dimensions[1].height = 30
        
        ws['A2'] = f"版本：2.0 (VBA增强版) | 创建日期：{datetime.now().strftime('%Y-%m-%d')}"
        ws['A2'].font = Font(size=10, color="666666")
        ws.merge_cells('A2:G2')
        ws['A2'].alignment = Alignment(horizontal='center')
        
        # VBA功能说明
        ws['A4'] = "🔥 VBA自动化功能"
        ws['A4'].font = Font(bold=True, size=13, color="C00000")
        ws.merge_cells('A4:G4')
        
        ws['A6'] = "本工具包含完整的VBA代码，实现以下自动化功能："
        ws.merge_cells('A6:G6')
        
        vba_features = [
            "✅ 自动生成投注方案 - 一键生成符合模板要求的投注号码",
            "✅ 自动判断中奖 - 输入开奖号码后自动比对并记录中奖情况",
            "✅ 自动更新历史 - 中奖记录自动保存到历史表",
            "✅ 智能验证 - 自动验证号码是否符合奇偶、大小、连号、同尾要求",
        ]
        
        row = 8
        for feature in vba_features:
            ws.cell(row, 1, feature).font = Font(size=10, bold=True)
            ws.merge_cells(f'A{row}:G{row}')
            row += 1
        
        # 使用步骤
        ws['A14'] = "📋 使用步骤（重要！）"
        ws['A14'].font = Font(bold=True, size=13, color="C55A11")
        ws.merge_cells('A14:G14')
        
        steps = [
            ("步骤1", "启用宏", "打开文件时选择【启用宏】或【启用内容】"),
            ("步骤2", "输入数据", "在【1-数据输入】表中输入最近30期开奖数据"),
            ("步骤3", "生成方案", "点击【开发工具】→【宏】→运行【生成投注方案】宏"),
            ("步骤4", "查看方案", "在【3-投注方案】表查看自动生成的投注号码"),
            ("步骤5", "执行投注", "按照生成的方案进行投注"),
            ("步骤6", "输入开奖", "在【4-开奖结果】表输入开奖号码"),
            ("步骤7", "判断中奖", "运行【判断中奖】宏，自动比对并记录中奖情况"),
            ("步骤8", "查看分析", "在【6-统计分析】表查看中奖统计"),
        ]
        
        row = 16
        for step, title, desc in steps:
            ws.cell(row, 1, step).font = Font(bold=True, size=10)
            ws.cell(row, 2, title).font = Font(bold=True, size=10, color="4472C4")
            ws.cell(row, 3, desc).font = Font(size=10)
            ws.merge_cells(f'C{row}:G{row}')
            ws.cell(row, 1).border = self.thin_border
            ws.cell(row, 2).border = self.thin_border
            ws.cell(row, 3).border = self.thin_border
            row += 1
        
        # 快捷按钮说明
        ws['A26'] = "⚡ 快捷操作（添加按钮后）"
        ws['A26'].font = Font(bold=True, size=13, color="70AD47")
        ws.merge_cells('A26:G26')
        
        ws['A28'] = "可在工作表中添加按钮来快速执行宏："
        ws.merge_cells('A28:G28')
        
        ws['A29'] = "• 在【3-投注方案】表添加【生成方案】按钮"
        ws['A30'] = "• 在【4-开奖结果】表添加【判断中奖】按钮"
        ws.merge_cells('A29:G29')
        ws.merge_cells('A30:G30')
        
        # 投注模板说明
        ws['A33'] = "📊 投注模板规则"
        ws['A33'].font = Font(bold=True, size=13, color="7030A0")
        ws.merge_cells('A33:G33')
        
        ws['A35'] = "模板A（80%使用频率）"
        ws['A35'].font = Font(bold=True, size=11)
        ws['A35'].fill = self.subheader_fill
        ws.merge_cells('A35:G35')
        
        template_a = [
            "• 奇偶比例：3奇 + 3偶",
            "• 大小比例：3小（1-16）+ 3大（17-33）",
            "• 连号限制：最多1组连号（如12,13）",
            "• 同尾限制：最多1组同尾（如03,13）",
        ]
        
        row = 36
        for item in template_a:
            ws.cell(row, 1, item).font = Font(size=10)
            ws.merge_cells(f'A{row}:G{row}')
            row += 1
        
        ws['A41'] = "模板B（20%使用频率）"
        ws['A41'].font = Font(bold=True, size=11)
        ws['A41'].fill = self.subheader_fill
        ws.merge_cells('A41:G41')
        
        template_b = [
            "• 奇偶比例：2奇 + 4偶",
            "• 大小比例：2小（1-16）+ 4大（17-33）",
            "• 连号限制：最多1组连号",
            "• 同尾限制：最多2组同尾",
        ]
        
        row = 42
        for item in template_b:
            ws.cell(row, 1, item).font = Font(size=10)
            ws.merge_cells(f'A{row}:G{row}')
            row += 1
        
        # 注意事项
        ws['A48'] = "⚠️ 重要注意事项"
        ws['A48'].font = Font(bold=True, size=13, color="C00000")
        ws.merge_cells('A48:G48')
        
        notes = [
            "1. 首次使用必须启用宏，否则自动化功能无法使用",
            "2. 必须输入完整30期数据才能生成准确的24码区间",
            "3. 每次新增数据后需要重新运行【生成投注方案】宏",
            "4. 开奖号码录入后运行【判断中奖】宏来更新中奖记录",
            "5. VBA代码仅供学习参考，投注方案不保证中奖",
            "6. 理性投注，不要沉迷，量力而行",
        ]
        
        row = 50
        for note in notes:
            ws.cell(row, 1, note).font = Font(size=10, color="666666")
            ws.merge_cells(f'A{row}:G{row}')
            row += 1
        
        # VBA代码导入说明
        ws['A58'] = "🔧 如何导入VBA代码"
        ws['A58'].font = Font(bold=True, size=13, color="4472C4")
        ws.merge_cells('A58:G58')
        
        import_steps = [
            "1. 按 Alt+F11 打开VBA编辑器",
            "2. 在左侧【工程】窗口找到本工作簿",
            "3. 右键点击工作簿名称 → 插入 → 模块",
            "4. 将VBA代码（见下方）复制粘贴到模块中",
            "5. 保存并关闭VBA编辑器",
            "6. 返回Excel，即可在【宏】列表中看到可用的宏",
        ]
        
        row = 60
        for step in import_steps:
            ws.cell(row, 1, step).font = Font(size=10)
            ws.merge_cells(f'A{row}:G{row}')
            row += 1
        
        ws['A68'] = "📄 VBA代码已自动生成在项目文件夹中："
        ws['A68'].font = Font(bold=True, size=11, color="70AD47")
        ws.merge_cells('A68:G68')
        
        ws['A69'] = "lottery_vba_code.txt - 完整的VBA代码"
        ws['A69'].font = Font(size=10, italic=True)
        ws.merge_cells('A69:G69')
        
        # 列宽
        ws.column_dimensions['A'].width = 10
        ws.column_dimensions['B'].width = 15
        for col in ['C', 'D', 'E', 'F', 'G']:
            ws.column_dimensions[col].width = 18
        
        return ws
    
    def create_input_sheet(self):
        """创建数据输入工作表"""
        ws = self.wb.create_sheet("1-数据输入")
        
        ws['A1'] = "双色球历史数据输入表"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:H1')
        
        ws['A2'] = "说明：请输入最近30期开奖数据（必须完整30期），输入后运行【生成投注方案】宏"
        ws['A2'].font = Font(italic=True, size=10, color="C00000")
        ws.merge_cells('A2:H2')
        
        headers = ['期号', '红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '蓝球']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(4, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = self.thin_border
        
        # 示例数据
        example_data = [
            ['2025001', 2, 3, 17, 18, 22, 33, 8],
            ['2025002', 5, 8, 12, 19, 26, 30, 11],
            ['2025003', 1, 7, 14, 21, 28, 32, 6],
        ]
        
        for row_idx, data in enumerate(example_data, 5):
            for col_idx, value in enumerate(data, 1):
                cell = ws.cell(row_idx, col_idx, value)
                cell.alignment = Alignment(horizontal='center')
                cell.border = self.thin_border
        
        for row in range(8, 35):
            for col in range(1, 9):
                cell = ws.cell(row, col)
                cell.border = self.thin_border
                cell.alignment = Alignment(horizontal='center')
        
        ws.column_dimensions['A'].width = 12
        for col in range(2, 9):
            ws.column_dimensions[get_column_letter(col)].width = 10
        
        return ws
    
    def create_analysis_sheet(self):
        """创建24码分析工作表"""
        ws = self.wb.create_sheet("2-24码分析")
        
        ws['A1'] = "24码主流区间自动分析"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:E1')
        
        ws['A2'] = "基于最近30期数据自动计算，取出现频次最高的前24个红球号码"
        ws['A2'].font = Font(italic=True, size=10, color="666666")
        ws.merge_cells('A2:E2')
        
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
        
        for num in range(1, 34):
            row = 4 + num
            ws.cell(row, 1, f"{num:02d}")
            count_formula = f'=COUNTIF(\'1-数据输入\'!B5:G34,A{row})'
            ws.cell(row, 2, count_formula)
            freq_formula = f'=B{row}/30'
            ws.cell(row, 3, freq_formula)
            ws.cell(row, 3).number_format = '0.00%'
            rank_formula = f'=RANK(B{row},B$5:B$37,0)'
            ws.cell(row, 5, rank_formula)
            selected_formula = f'=IF(E{row}<=24,"✓","")'
            ws.cell(row, 4, selected_formula)
            
            for col in range(1, 6):
                ws.cell(row, col).alignment = Alignment(horizontal='center')
                ws.cell(row, col).border = self.thin_border
        
        ws['G4'] = "24码主流区间"
        ws.merge_cells('G4:K4')
        ws['G4'].font = self.header_font
        ws['G4'].fill = self.header_fill
        ws['G4'].alignment = Alignment(horizontal='center')
        
        for i in range(24):
            row = 5 + i
            formula = f'=IFERROR(INDEX(A$5:A$37,MATCH(SMALL(E$5:E$37,{i+1}),E$5:E$37,0)),"")'
            ws.cell(row, 7, formula)
            ws.cell(row, 7).alignment = Alignment(horizontal='center')
            ws.cell(row, 7).border = self.thin_border
            ws.cell(row, 7).fill = self.highlight_fill
        
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
        
        ws['A1'] = "自动生成投注方案（VBA自动化）"
        ws['A1'].font = Font(bold=True, size=14, color="C00000")
        ws.merge_cells('A1:J1')
        
        ws['A2'] = "运行【生成投注方案】宏来自动生成投注号码"
        ws['A2'].font = Font(italic=True, size=11, color="C00000", bold=True)
        ws.merge_cells('A2:J2')
        
        ws['A4'] = "模板A（80%）："
        ws['B4'] = "3奇3偶 + 3小3大 + 连号≤1组 + 同尾≤1组"
        ws['A5'] = "模板B（20%）："
        ws['B5'] = "2奇4偶 + 2小4大 + 连号≤1组 + 同尾≤2组"
        
        for row in [4, 5]:
            ws.cell(row, 1).font = self.bold_font
            ws.cell(row, 2).font = Font(size=10, color="666666")
        
        headers = ['期号', '注号', '模板', '红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '蓝球']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(7, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
        ws['L7'] = "方案生成说明"
        ws['L7'].font = self.header_font
        ws['L7'].fill = self.subheader_fill
        ws.merge_cells('L7:N7')
        
        instructions = [
            "1. 确保输入表有30期数据",
            "2. 运行【生成投注方案】宏",
            "3. 每期自动生成10注",
            "4. 8注使用模板A",
            "5. 2注使用模板B",
            "6. 自动填充蓝球（1-16）",
        ]
        
        for idx, inst in enumerate(instructions, 8):
            ws.cell(idx, 12, inst).font = Font(size=9)
            ws.merge_cells(f'L{idx}:N{idx}')
        
        ws.column_dimensions['A'].width = 12
        for col in range(2, 11):
            ws.column_dimensions[get_column_letter(col)].width = 9
        
        return ws
    
    def create_draw_result_sheet(self):
        """创建开奖结果工作表"""
        ws = self.wb.create_sheet("4-开奖结果")
        
        ws['A1'] = "开奖结果输入与中奖判断"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:I1')
        
        ws['A2'] = "输入开奖号码后，运行【判断中奖】宏自动判断中奖情况"
        ws['A2'].font = Font(italic=True, size=11, color="C00000", bold=True)
        ws.merge_cells('A2:I2')
        
        headers = ['期号', '开奖红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '开奖蓝球', '录入时间']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(4, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
        for row in range(5, 55):
            ws.cell(row, 1, f'=\'1-数据输入\'!A{row}')
            for col in range(1, 10):
                ws.cell(row, col).alignment = Alignment(horizontal='center')
                ws.cell(row, col).border = self.thin_border
        
        ws.column_dimensions['A'].width = 12
        for col in range(2, 10):
            ws.column_dimensions[get_column_letter(col)].width = 11
        
        return ws
    
    def create_history_sheet(self):
        """创建历史记录工作表"""
        ws = self.wb.create_sheet("5-历史记录")
        
        ws['A1'] = "投注与中奖历史记录（自动更新）"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:M1')
        
        headers = ['期号', '注号', '投注红球', '投注蓝球', '开奖红球', '开奖蓝球', 
                   '中红球数', '中蓝球', '中奖等级', '奖金', '投入', '盈亏', '备注']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(3, col, header)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = self.thin_border
        
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
        
        ws['A1'] = "数据统计与分析报告"
        ws['A1'].font = Font(bold=True, size=14)
        ws.merge_cells('A1:F1')
        
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
        
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 12
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 12
        ws.column_dimensions['F'].width = 10
        ws.column_dimensions['G'].width = 10
        ws.column_dimensions['H'].width = 12
        
        return ws
    
    def generate(self, filename="双色球投注方案生成工具_VBA版.xlsx"):
        """生成完整的Excel工具"""
        print("正在创建Excel工作簿（VBA增强版）...")
        
        print("创建使用说明工作表...")
        self.create_instruction_sheet_vba()
        
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
        
        # 保存VBA代码到文本文件
        vba_file = "lottery_vba_code.txt"
        with open(vba_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("双色球投注方案生成工具 - VBA代码\n")
            f.write("=" * 60 + "\n\n")
            f.write("使用方法：\n")
            f.write("1. 打开Excel文件\n")
            f.write("2. 按 Alt+F11 打开VBA编辑器\n")
            f.write("3. 插入新模块（Insert → Module）\n")
            f.write("4. 将下面的代码复制粘贴到模块中\n")
            f.write("5. 保存并关闭VBA编辑器\n\n")
            f.write("=" * 60 + "\n\n")
            f.write(self.get_vba_code())
        
        print(f"✅ VBA代码已保存为：{vba_file}")
        
        return filename


def main():
    """主函数"""
    print("=" * 60)
    print("双色球投注方案生成Excel工具（VBA增强版）")
    print("=" * 60)
    
    generator = LotteryExcelGeneratorVBA()
    filename = generator.generate()
    
    print("\n" + "=" * 60)
    print("工具已生成，包含以下工作表：")
    print("  0. 使用说明 - 完整的使用指南和VBA导入说明")
    print("  1. 数据输入 - 输入最近30期开奖数据")
    print("  2. 24码分析 - 自动分析生成24码主流区间")
    print("  3. 投注方案 - VBA自动生成投注方案")
    print("  4. 开奖结果 - 输入开奖号码")
    print("  5. 历史记录 - 自动保存中奖历史")
    print("  6. 统计分析 - 多维度数据分析报告")
    print("=" * 60)
    print("\n🔥 VBA自动化功能：")
    print("  • 【生成投注方案】宏 - 自动生成符合模板要求的投注号码")
    print("  • 【判断中奖】宏 - 自动比对开奖号码并记录中奖情况")
    print("=" * 60)
    print("\n📌 下一步：")
    print("1. 打开生成的Excel文件")
    print("2. 启用宏（点击【启用内容】按钮）")
    print("3. 按 Alt+F11 打开VBA编辑器")
    print("4. 将 lottery_vba_code.txt 中的代码导入到新模块")
    print("5. 在【1-数据输入】表中输入30期数据")
    print("6. 运行【生成投注方案】宏开始使用")
    print("=" * 60)


if __name__ == "__main__":
    main()
