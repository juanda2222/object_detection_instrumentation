from get_data import get_data
def get_vector() :
   T1R1=1
   T1R2=0
   T2R1=0 
   T2R2=0
   
   list_T1R1,list_T1R2,list_T2R1,list_T2R2=get_data()
   if T1R1 == 1 and T1R2 == 0 and T2R1 == 0 and T2R2 == 0 :
      vector1 = list_T1R1         
      vector2 = [0]         
      vector3 = [0]         
      vector4 = [0]         
      return vector1,vector2,vector3,vector4

   if T1R1 == 1 and T1R2 == 1 and T2R1 == 0 and T2R2 == 0 :
      #[list_T1R1.append(i) for i in list_T1R2]
      vector1 = list_T1R1
      vector2 = list_T1R2
      vector3 = [0]
      vector4 = [0]

      return vector1,vector2,vector3,vector4
    
   if T1R1 == 1 and T1R2 == 0 and T2R1 == 1 and T2R2 == 0 :
      #[list_T1R1.append(i) for i in list_T2R1]
      vector1 = list_T1R1
      vector2 = [0]
      vector3 = list_T2R1
      vector4 = [0]
      return vector1,vector2,vector3,vector4
 
   if T1R1 == 1 and T1R2 == 1 and T2R1 == 1 and T2R2 ==1 :
      #[list_T1R1.append(i) for i in list_T1R2]
      #[list_T1R1.append(i) for i in list_T2R1]
      #[list_T1R1.append(i) for i in list_T2R2]
      vector1 = list_T1R1
      vector2 = list_T1R2
      vector3 = list_T2R1
      vector4 = list_T2R2
      ##print(len(vector))
      return vector1,vector2,vector3,vector4


#vector= get_vector()
#print("Vector1 :", vector)
#print("longitud Vector1 :", len(vector))
