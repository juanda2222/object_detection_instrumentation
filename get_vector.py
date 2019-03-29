from get_data import get_data
def get_vector() :
   T1R1=1
   T1R2=1
   T2R1=0 
   T2R2=0
   
   list_T1R1,list_T1R2,list_T2R1,list_T2R2=get_data()
   if T1R1 == 1 and T1R2 == 0 and T2R1 == 0 and T2R2 == 0 :
      vector = list_T1R1         
      return vector

   if T1R1 == 1 and T1R2 == 1 and T2R1 == 0 and T2R2 == 0 :
      [list_T1R1.append(i) for i in list_T1R2]
      vector = list_T1R1         
      return vector
    
   if T1R1 == 1 and T1R2 == 0 and T2R1 == 1 and T2R2 == 0 :
      [list_T1R1.append(i) for i in list_T2R1]
      vector = list_T1R1
      return vector
 
   if T1R1 == 1 and T1R2 == 1 and T2R1 == 1 and T2R2 ==1 :
      [list_T1R1.append(i) for i in list_T1R2]
      [list_T1R1.append(i) for i in list_T2R1]
      [list_T1R1.append(i) for i in list_T2R2]
      vector = list_T1R1
      ##print(len(vector))
      return vector


#vector= get_vector()
#print("Vector1 :",vector)
