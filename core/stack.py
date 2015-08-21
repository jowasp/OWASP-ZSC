#!/usr/bin/env python
'''
OWASP ZSC | ZCR Shellcoder

ZeroDay Cyber Research
Z3r0D4y.Com
Ali Razmjoo
'''
def st(data):
	return data[::-1].encode('hex')
def generate(data,register,gtype):
	length = len(data)
	if gtype == 'int':
		try:
			data = hex(int(data, 8))
		except:
			data = hex(int(data, 16))
	if gtype == 'string':
		data = st(data)
	if length <= 3:
		if gtype == 'string':
			data = str('0x') + str(data)
		if len(data) % 2 is not 0:
			data = data.replace('0x','0x0')
		if len(data) is 8:
			data = data + '90\npop %s\nshr $0x8,%s\npush %s\n'%(register,register,register)
		if len(data) is 6:
			data = data + '9090\npop %s\nshr $0x10,%s\npush %s\n'%(register,register,register)
		if len(data) is 4:
			data = data + '909090\npop %s\nshr $0x10,%s\nshr $0x8,%s\npush %s\n'%(register,register,register,register)
		data = str('push $') + str(data)
	if length >= 4:
		if gtype == 'int':
			data = data[2:]
		stack_content = data
		shr_counter = len(stack_content) % 8
		shr = None
		if shr_counter is 2:
			shr = '\npop %s\nshr    $0x10,%s\nshr    $0x8,%s\npush %s\n'%(register,register,register,register)
			stack_content = stack_content[0:2] + '909090' + stack_content[2:]
		if shr_counter is 4:
			shr = '\npop %s\nshr    $0x10,%s\npush %s\n'%(register,register,register)
			stack_content = stack_content[0:4] + '9090' + stack_content[4:]
		if shr_counter is 6:
			shr = '\npop %s\nshr    $0x8,%s\npush %s\n'%(register,register,register)
			stack_content = stack_content[0:6] + '90' + stack_content[6:]
		zshr = shr
		m = len(stack_content)
		n = len(stack_content) / 8
		file_shellcode = ''
		if (len(stack_content) % 8) is 0:
			shr_n = 0
			r = ''
			while(n is not 0):
				if shr is not None:
					shr_n += 1
					zx = m - 8
					file_shellcode = 'push $0x' + str(stack_content[zx:m]) + '\n' + file_shellcode 
					m -= 8
					n = n - 1
					shr = None
				if shr is None:
					shr_n += 1
					zx = m - 8
					file_shellcode =  'push $0x' + str(stack_content[zx:m]) + '\n' + file_shellcode
					m -= 8
					n = n - 1
			if zshr is None:
				file_z = file_shellcode
			if zshr is not None:
				rep1 = file_shellcode[:16]
				rep2 = rep1 + zshr
				file_z = file_shellcode.replace(rep1,rep2)
		data = file_z
	return data