##training  data
sentence1=['D1','T1','M1','P1','M2','P2']
correct_set1=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])

sentence2=['D1','T1','M1','M2','P1','P2']
correct_set2=(['D1','T1','M1','P1'],['D1','T2','M2','P2'],['D1','T1','M2','P1'],['D1','T2','M1','P2'])

sentence3=['D1','T1','M1','P1']
correct_set3=(['D1','T1','M1','P1'])

sentence4=['D1','M1','T1','P1','P2']
correct_set4=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])

sentence5=['D1','T1','M1','P1','M2','P2']
correct_set5=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])

sentence6=['D1','T1','P1','M1']
correct_set6=(['D1','T1','M1','P1'])

sentence7=['D1','T1','M1','P1','P2']
correct_set7=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])

sentence8=['D1','T1','T2','T3','M1','P1']
correct_set8=(['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'])

sentence9=['D1','T1','T2','T3','T4','M1','P1','P2']
correct_set9=(['D1','T1','M1','P1'],['D1','T2','M1','P1'],['D1','T3','M1','P1'],['D1','T4','M1','P1'],['D1','T1','M1','P2'],['D1','T2','M1','P2'],['D1','T3','M1','P2'],['D1','T4','M1','P2'])

sentence10=['D1','T1','M1','P1','M2','P2']
correct_set10=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])

sentence11=['D1','T1','M1','P1','P2']
correct_set11=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])

sentence12=['D1','T1','M1','P1','M2','P2']
correct_set12=(['D1','T1','M1','P1'],['D1','T2','M2','P2'])

sentence13=['D1','T1','M1','P1','P2','P3']
correct_set13=(['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3'])

sentence14=['D1','T1','M1','P1','M2','P2']
correct_set14=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])

sentence15=['D1','T1','M1','P1','P2']
correct_set15=(['D1','T1','M1','P1'],['D1','T1','M1','P2'])

sentence16=['D1','T1','M1','T2','M2','P1']
correct_set16=(['D1','T1','M1','P1'],['D1','T2','M2','P1'])

sentence17=['D1','T1','M1','P1','P2','P3']
correct_set17=(['D1','T1','M1','P1'],['D1','T1','M1','P2'],['D1','T1','M1','P3'])

sentence18=['D1','T1','M1','P1','M2','P2']
correct_set18=(['D1','T1','M1','P1'],['D1','T1','M2','P2'])


# sentence19=['D1', 'P1', 'A1', 'T1']
# correct_set19=(['D1', 'P1', 'A1', 'T1'])
# 
# sentence20=['D1', 'P1', 'P2', 'P3', 'D2', 'P4', 'D3', 'T1', 'R1', 'T2', 'R2', 'T3', 'R3', 'T4', 'R4', 'T5', 'R5', 'T6', 'R6', 'T7', 'R7', 'P5', 'A1']
# correct_set20=([ 'D3','P4','T1', 'R1'],['D3','P4','T2','R2'],['D3', 'P4','T3', 'R3'],['D3','P4', 'T4', 'R4'],['D3','P4', 'T5', 'R5'],['D3', 'P4','T6', 'R6'],['D3','P4', 'T7', 'R7'])
# 
# sentence21=['T1', 'P1', 'D1', 'R1', 'A1']
# correct_set21=(['T1', 'P1', 'D1', 'R1'])
# 
# sentence22=['D1', 'A1', 'T1', 'P1']
# correct_set22=(['D1', 'A1', 'T1', 'P1'])
# 
# sentence23=['D1', 'T1', 'P1', 'A1']
# correct_set23=(['D1', 'T1', 'P1', 'A1'])
# 
# sentence24=['D1', 'P1', 'P2', 'T1', 'R1', 'A1']
# correct_set24=(['D1', 'P1', 'T1', 'R1'] ,['D1', 'P2', 'T1', 'R1'])
# 
# sentence25=['D1', 'A1', 'P1', 'T1', 'T2']
# correct_set25=(['D1','A1','P1','T1'],['D1','A1','P1','T2'])
# 
# sentence26=['P1', 'T1', 'P2', 'R1', 'D1', 'T2', 'P3', 'R2', 'A1', 'D2', 'D3', 'P4', 'D4', 'P5', 'P6']
# correct_set26=(['D1', 'T2', 'P3', 'R2'])
# 
# sentence27=['D1', 'P1', 'P2', 'T1', 'R1']
# correct_set27=(['D1','T1','R1','P1'],['D1','T1','R1','P2'])
# 
# sentence28=['D1', 'A1', 'P1', 'T1', 'R1', 'T2', 'R2']
# correct_set28=(['D1','T1','R1','P1'],['D1','T2','R2','P1'])
# 
# sentence29=['D1', 'T1', 'A1', 'P1', 'P2']
# correct_set29=(['D1','T1','A1','P1'],['D1','T1','A1','P2'])
# 
# sentence30=['D1', 'A1', 'P1', 'P2', 'T1', 'A2', 'P3', 'P4', 'P5']
# correct_set30=(['D1','T1','A1','P1'],['D1','T1','A1','P2'])
# 
# sentence31=['D1', 'P1', 'A1', 'T1', 'R1']
# correct_set31=(['D1','T1','R1','P1'])