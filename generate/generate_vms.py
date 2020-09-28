import random
import csv
import config

csv_columns    = config.csv_columns
fake_vms_count = config.fake_vms_count
user_filename  = config.user_filename
csv_vm_file    = config.csv_vm_file
csv_vm_columns = config.csv_vm_columns

role_index     = csv_columns.index("role")
empid_index    = csv_columns.index("empid")

filter_role    = 'Product Owner'

reader = csv.reader(open(user_filename),delimiter=',')
filtered = list(filter(lambda p: filter_role == p[role_index], reader))
print(f'Total {filter_role} are {len(filtered)}')
filter_role_userlist = []

for f in filtered:
    #print(f[0],f[3])
    filter_role_userlist.append(f[empid_index])
#print(filter_role_userlist)

with open(csv_vm_file,'w') as f1:
    writer=csv.writer(f1, delimiter=',',lineterminator='\n',)
    writer.writerow(csv_vm_columns)
    for i in range(1,fake_vms_count+1):
        row = ['V'+'{:05d}'.format(i),random.choice(filter_role_userlist)]
        writer.writerow(row)

print(f'Generated {csv_vm_file} with {fake_vms_count} VMs')