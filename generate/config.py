#No of users to create
fake_users_count = 100

#Organization Domain Name
domain = 'kanakjr.in'

#Department - Available Departments in the Organization  
departments = ['HR','IT','SUPPORT','SECURITY','MANAGEMENT']
departments_distrib = [5,30,35,20,10] #Given in % 
departments_distrib_dict = {departments[i]: departments_distrib[i] for i in range(len(departments))} 

#Roles - Available Roles in each Department
roles = {'IT':['Developer','Tester','Team Lead'],
         'SUPPORT':['L0','L1','l2'],
         'HR':['HR Head','HR'],
         'SECURITY':['Admins','Analyst','Pentester'],
         'MANAGEMENT':['Product Owner','Delivery Head','CISO','CEO']}
roles_limit = {'CEO':1,'CISO':1,'HR Head':1,'Delivery Head':1}
roles_limit['Team Lead'] = int(departments_distrib_dict['IT']/10) # 10% Lead in total IT department

#Manages - Define which Role manages other Role
manages = {
'CEO':['Product Owner','CISO','Delivery Head','HR Head'],
'Delivery Head':['L0','L1','l2'],
'CISO':['SOC Monitor','Analyst','Pentester'],
'HR Head':['HR'],
'Product Owner':['Team Lead'],
'Team Lead':['Developer','Tester']
}