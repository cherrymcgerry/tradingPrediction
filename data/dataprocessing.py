import pandas as pd
import matplotlib
import bs4 as bs
import pandas_datareader.data as web
import pickle
import requests
import os
import cv2
import datetime as dt


# ofwel dict als input ofwel enkel data?

def labelDataFromTicker(dict):
    TIMEPERIOD = 30
    LASTDAY = TIMEPERIOD -1


    df = dict['df']
    dfClose = df[['Close']]
    ticker = dict['ticker']

    resultDict = { 'ticker' : ticker, 'data' : []  }

    for index, day in enumerate(df):
        if len(df.index) < (index + TIMEPERIOD):
            periodData = df.iloc[index:(index + LASTDAY)]
            priceLbl = dfClose.iloc[(index + TIMEPERIOD)]
            if dfClose.iloc[(index + LASTDAY)] > priceLbl:
                boolLbl = True
            else:
                boolLbl = False
            resultDict['data'].append({'labelPrice': priceLbl, 'labelBool' : boolLbl, 'periodData': periodData})

    return resultDict


def generateImages(dict):
    ROOT = 'inputData'
    TICKERPATH = os.path.join(ROOT, dict['ticker'])
    #make folder
    if not os.path.isdir(ROOT):
        os.mkdir(ROOT)
    os.mkdir(TICKERPATH)
    print(F'generating images for {dict["ticker"]}')

    priceLblDict = []
    boolLblDict = []

    #loop over data -> make images per period save them and save a file with the labels and the corresponding image name
    for index, data in enumerate(dict['data']):
        priceLabel = data['labelPrice']
        boolLabel = data['labelBool']
        periodData = data['periodData']

        #Generate imgs according to different indexes  -> try to make them black and white
        imgs = []

        #concatenate imgs to one image

        # img = img.convert("L")   #converts to grayscale
        #split all images into seperate channels  -> black and white so should be one channnel already so maybe this is not necessary
        b_channel, g_channel, r_channel = cv2.split(img)

        #this is the channel to add just as example
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50  # creating a dummy alpha channel image.

        #mergo to merge channels into one image
        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

        imagePath = os.path.join(TICKERPATH, F'image{index}.jpg')
        #save img to specific path
        img.save(imagePath)

        #link labels to imagePath
        priceLblDict.append([priceLabel, imagePath])
        boolLblDict.append([boolLabel,imagePath])

    with open(os.path.join(TICKERPATH,'priceLabels.data'),'wb') as f:
        pickle.dump(priceLblDict,f)
    with open(os.path.join(TICKERPATH, 'boolLabels.data'), 'wb') as f:
        pickle.dump(boolLblDict, f)





