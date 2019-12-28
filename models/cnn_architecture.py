import torch.nn as nn
import numpy as np
import torchvision as tv

class CNN(nn.Module):
    def __init__(self,di,do ,conv_layers,fc_layers, use_resnet=False):  #di -> dimensions input,   do -> dimensions output

        super(CNN,self).__init__()
        submodule = None

        if use_resnet:
            submodule = tv.models.resnet50(pretrained=True, progress=False)

        if submodule is None:
            submodule = DownConv(di,do)

        for i in range(1,conv_layers):
            prev_do_mult = do_mult
            do_mult = min(2 ** i,16)
            submodule = DownConv(do*prev_do_mult,do*do_mult,submodule=submodule)

 # slechts 1 output want ie moet close meegeven. Ook eens proberen met ipv close enkel buy, sell of hold maar dan moeten labels anders
        submodule = DownConv(do*do_mult,1,final=True,submodule=submodule)

        softmax = nn.Softmax(dim=1)
        model = [submodule]+ [softmax]

        self.main = nn.Sequential(*model)



class DownConv(nn.Module):
    def __init__(self, di,do, kernel=4,final=False, submodule=None):
        super(DownConv,self).__init__()
        conv = nn.Conv2d(di,do, kernel_size=kernel, stride=2,padding=1,bias=False)
        norm = nn.BatchNorm2d(do)
        relu = nn.LeakyReLU(0.01,True)
        dropout = nn.Dropout(0.5)
        layer = [conv,norm,relu]
        if submodule is None:
            model = [conv,relu]
        elif final:
            model = [submodule] + [dropout,conv]
        else:
            model = [submodule] + layer
        self.main = nn.Sequential(*model)

    def forward(self,x):
        return self.main(x)


