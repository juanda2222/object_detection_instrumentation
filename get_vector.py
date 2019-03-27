from get_data import get_data
def get_vector() :
   T1R1=1
   T1R2=1
   T2R1=0 
   T2R2=0
   count=0
   
   if T1R1 == 1 and T1R2 == 0 and T2R1 == 0 and T2R2 == 0 :
      n=1
      count = 0
      while count <= n :
         list_T1R1,list_T1R2,list_T2R1,list_T2R2=get_data()
         if n == count :
            return list_T1R1,list_T1R2,list_T2R1,list_T2R2
         count += 1

   if T1R1 == 1 and T1R2 == 1 and T2R1 == 0 and T2R2 == 0 :
      n=2
      count = 0
      while count <= n :
         list_T1R1,list_T1R2,list_T2R1,list_T2R2=get_data()
         if count == 0:
            list_T1R11 = list_T1R1.copy()
         if count == 1 :
            return list_T1R11,list_T1R2,list_T2R1,list_T2R2
         count += 1
   if T1R1 == 1 and T1R2 == 0 and T2R1 == 1 and T2R2 == 0 :
      n=2
      count = 0      
      while count <= n :
         list_T1R1,list_T1R2,list_T2R1,list_T2R2=get_data()
         if count == 0:
            list_T1R11 = list_T1R1.copy()
         if count == 1 :
            return list_T1R11,list_T1R2,list_T2R1,list_T2R2
         count += 1

   if T1R1 == 1 and T1R2 == 1 and T2R1 == 1 and T2R2 ==1 :
      n=4
      count = 0
      while count <= n :
         list_T1R1,list_T1R2,list_T2R1,list_T2R2=get_data()              
         if count == 0:
            list_T1R11 = list_T1R1.copy()
         if count == 1:
            list_T1R22 = list_T1R2.copy()
         if count == 2:
            list_T2R11 = list_T2R1.copy()
         if count == 3 :
            return list_T1R11,list_T1R22,list_T2R11,list_T2R2
         count += 1

vector1,vector2,vector3,vector4 = get_vector()
#print(vector)
print(vector1)
print(vector2)
print(vector3)
print(vector4)