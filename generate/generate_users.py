import random
import collections
import json
from faker import Faker
import csv

fake_users_count = 100
fake = Faker('en_IN')
domain = 'kanakjr.in'

departments = ['HR','IT','SUPPORT','SECURITY','MANAGEMENT']
departments_distrib = [5,30,35,20,10] 
departments_distrib_dict = {departments[i]: departments_distrib[i] for i in range(len(departments))} 

roles = {'IT':['Developer','Tester','Team Lead'],
         'SUPPORT':['L0','L1','l2'],
         'HR':['HR Head','HR'],
         'SECURITY':['SOC Monitor','Analyst','Pentester'],
         'MANAGEMENT':['Product Owner','Delivery Head','CISO','CEO']}
roles_limit = {'CEO':1,'CISO':1,'HR Head':1,'Delivery Head':1}
roles_limit['Team Lead'] = int(departments_distrib_dict['IT']/10) # 10% lead in total IT department
roles_assigned = []

manages = {
'CEO':['Product Owner','CISO','Delivery Head','HR Head'],
'Delivery Head':['L0','L1','l2'],
'CISO':['SOC Monitor','Analyst','Pentester'],
'HR Head':['HR'],
'Product Owner':['Team Lead'],
'Team Lead':['Developer','Tester']
}
# manages = {'Team Lead':['Developer','Tester']}


def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]


def gen_department():
    return random.choice(departments)

def gen_role(department):
    for role,limit in roles_limit.items():
        if role in roles[department]: 
            if limit>0:
                roles_limit[role]=roles_limit[role]-1
                return role
            elif limit==0:
                roles_assigned.append(role)
    role_choices = set(roles[department])-set(roles_assigned)
    return random.choice(list(role_choices))

profiles_lst = {}
for dept,dist in zip(departments,departments_distrib):
    dept_users_count = int(fake_users_count*dist/100)
    #print(dept,dept_users_count)
    for _ in range(dept_users_count):
        firstname  = fake.first_name()
        lastname   = fake.last_name()
        fullname   = firstname+' '+lastname
        userid     = str.lower(firstname+'_'+lastname+'@'+domain)
        empid      = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        #birthdate  = fake.date_of_birth()
        department = dept #gen_department()
        role       = gen_role(department)
        profile = {'firstname':firstname,'lastname':lastname,'fullname':fullname,
        'userid':userid,'empid':empid,
        #'birthdate':birthdate,
        'department':department,'role':role
        #,'manages':[],
        ,'managedby':[]
        }
        profiles_lst[empid] = profile

print(f'Generated {len(profiles_lst)} number of profiles')

profiles_lst_dept = [value["department"] for key,value in profiles_lst.items()]
profiles_lst_roles = [value["role"] for key,value in profiles_lst.items()]
print(f'\nDepartment: {collections.Counter(profiles_lst_dept).most_common()}')
print(f'\nRoles: {collections.Counter(profiles_lst_roles).most_common()}')
print('')

for manages,managedby in manages.items():
    #print('\n----',manages,managedby,'----')
    manages_user_lst = []
    managedby_user_lst = []
    # print(manages,managedby)
    for empid,p in profiles_lst.items():
        if p['role'] == manages:
            manages_user_lst.append(p['empid'])
        elif p['role'] in managedby:
            managedby_user_lst.append(p['empid'])
    #print(manages_user_lst)
    #print(managedby_user_lst)
    count_manages = len(manages_user_lst)
    count_managedby = len(managedby_user_lst)
    print(count_manages,manages,'-- manages ->',count_managedby,managedby)

    partition_managedby_user_lst = partition(managedby_user_lst,len(manages_user_lst))
    #print('partition_managedby_user_lst',partition_managedby_user_lst)
    #print('partition_managedby_user_lst',len(partition_managedby_user_lst))
    
    for m,mb_lst in zip(manages_user_lst,partition_managedby_user_lst):
        for mb in mb_lst:
            #profiles_lst[m]['manages'].append(mb)
            profiles_lst[mb]['managedby'].append(m)
            #print(m,mb)

# with open('users.json', 'w') as fp: json.dump(profiles_lst, fp)

csv_file = "Users.csv"
csv_columns = ['empid','firstname','lastname','fullname','userid','department','role',
# 'manages',
'managedby']

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for empid,data in profiles_lst.items():
            #data['manages'] = ';'.join(data['manages'])
            data['managedby'] = ';'.join(data['managedby'])
            writer.writerow(data)
except IOError:
    print("I/O error")


