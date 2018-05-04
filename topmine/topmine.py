import subprocess, shlex

def get_output_of(command):
	args = shlex.split(command)
	return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
 
file_name = "input/data.txt"
num_topics=150

phrase_mining_cmd = "python topmine_src/run_phrase_mining.py {0}".format(file_name)
print(get_output_of(phrase_mining_cmd))

phrase_lda_cmd = "python topmine_src/run_phrase_lda.py {0}".format(num_topics)
print(get_output_of(phrase_lda_cmd))

