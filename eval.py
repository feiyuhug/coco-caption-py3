# -*- coding: utf-8 -*-
# requires python 2.7
from __future__ import print_function

import sys
import json

from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap


def evaluation(annotation_file, result_file):
    coco = COCO(annotation_file)
    cocoRes = coco.loadRes(result_file)
    # create cocoEval object by taking coco and cocoRes
    cocoEval = COCOEvalCap(coco, cocoRes)

    # evaluate on a subset of images by setting
    # cocoEval.params['image_id'] = cocoRes.getImgIds()
    # please remove this line when evaluating the full validation set
    cocoEval.params['image_id'] = cocoRes.getImgIds()

    # evaluate results
    # SPICE will take a few minutes the first time, but speeds up due to caching
    cocoEval.evaluate()

    # print output evaluation scores
    for metric, score in cocoEval.eval.items():
        print('%s: %.3f' % (metric, score))

    # demo how to use evalImgs to retrieve low score result
    # evals = [eva for eva in cocoEval.evalImgs if eva['CIDEr'] < 30]
    # print('ground truth captions')
    # imgId = evals[0]['image_id']
    # annIds = coco.getAnnIds(imgIds=imgId)
    # anns = coco.loadAnns(annIds)
    # coco.showAnns(anns)


if __name__ == '__main__':
    evaluation(r"D:\Code\Sources\ML\coco-caption-py3\coco-caption-master\annotations\captions_val2014.json",
               r"D:\Code\Sources\ML\coco-caption-py3\coco-caption-master\results\captions_val2014_fakecap_results.json")