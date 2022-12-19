import subprocess
type_list = open('./word/type.txt','r').read().split("\n")
adjective_list = open('./word/adjective.txt','r').read().split("\n")
color_list = open('./word/color.txt','r').read().split("\n")
object_list = open('./word/object.txt','r').read().split("\n")
#どんな感じのモデル形態で〇〇のような△色のxx
epochs = [2500,5000]
learning_rate = [0.001,0.01,0.1]
i = 0
#print(object_list)
#print("object_listの配列数:",len(object_list))
#print("adjective_listの配列数:",len(adjective_list))
#print("color_listの配列数:",len(color_list))

for len_type in range(len(type_list)):
    for len_obj in range(len(object_list)):
        for num_epoch in range(len(epochs)):
            for num_lr in range(len(learning_rate)):
                epoch = epochs[num_epoch]
                lr = learning_rate[num_lr]
                text = type_list[len_type] + " " + object_list[len_obj]
                output_path = "/outputs/"+type_list[len_type] + "_" + object_list[len_obj] + "_" + str(epoch) + "_" + str(lr) + "/"
                cmd = 'python /clipmesh/main.py --config configs/single2jp.yml  --text_prompt \"{0}\" --output_path \"{1}\" --epochs {2} --lr {3}'.format(text,output_path,epoch,lr)
                subprocess.run(cmd,shell=True,stderr=subprocess.STDOUT)
                i += 1
                print(str(i) + "回目")
# for len_type in range(len(type_list)):
#     for len_adj in range(len(adjective_list)):
#         for len_col in range(len(color_list)):
#             for len_obj in range(len(object_list)):
#                 text = type_list[len_type] + " " + adjective_list[len_adj] + " " + color_list[len_col] + " " + object_list[len_obj]
#                 output_path = "/output/"+type_list[len_type] + "/" + adjective_list[len_adj] + "/" + color_list[len_col] + "/" + object_list[len_obj] + "/"
#                 cmd = 'main.py --config configs/single2jp.yml  --text_prompt \"{0}\" --output_path \"{1}\"'.format(text,output_path) 
#                 #python main.py --config configs/single2jp.yml  --text_prompt {} 



