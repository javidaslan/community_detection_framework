import datetime

from openpyxl import Workbook
from openpyxl.styles import Font


def create_report(results, algorithm):
    """
    Create Excel report with following data
    """
    print("Creating report for results")
    
    wb = Workbook()
    ws = wb.active

    ws['A1'].value = 'Algorithm: {0}'.format(algorithm) 
    ws['A3'].value = 'Number of Nodes'
    ws['B3'].value = 'Number of Edges'
    ws['C3'].value = 'Degree'
    ws['D3'].value = 'Gamma'
    ws['E3'].value = 'Beta'
    ws['F3'].value = 'MU'
    ws['G3'].value = 'GT Communities'
    ws['H3'].value = 'Communities Found'
    ws['I3'].value = 'NMI'
    ws['J3'].value = 'ARI'
    ws['K3'].value = 'VI'
    ws['L3'].value = 'Purity'

    for col in range(12):
        ws.cell(row=1, column=col+1).font = Font(bold=True, size=12)

    for ind, result in enumerate(results):
        ws['A'+str(ind+4)].value = result[0]
        ws['B'+str(ind+4)].value = result[1]
        ws['C'+str(ind+4)].value = result[2]
        ws['D'+str(ind+4)].value = result[3]
        ws['E'+str(ind+4)].value = result[4]
        ws['F'+str(ind+4)].value = result[5]
        ws['G'+str(ind+4)].value = result[6]
        ws['H'+str(ind+4)].value = result[7]
        ws['I'+str(ind+4)].value = result[8]
        ws['J'+str(ind+4)].value = result[9]
        ws['K'+str(ind+4)].value = result[10]
        ws['L'+str(ind+4)].value = result[11]

    file_name = datetime.datetime.now().strftime("%d%m%Y%H%M%S") + '.xlsx'
    wb.save(file_name)
    wb.close

    print("Report generated")