# -*- coding: utf-8 -*-
# requires python 2.7
from __future__ import print_function

import sys
import json
import os
import re

from nltk.tokenize.stanford_segmenter import StanfordSegmenter

from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap


class StanfordTokenizer:
    """
    class for segmenting Chinese sentences
    """
    def __init__(self):
        stanford_corenlp_path = r'D:\Desktop\stanford corenlp'
        self.segmenter = StanfordSegmenter(
            java_class=r"edu.stanford.nlp.ie.crf.CRFClassifier",
            path_to_jar=os.path.join(stanford_corenlp_path, 'stanford-segmenter-2018-02-27', 'stanford-segmenter-3.9.1.jar'),
            path_to_slf4j=os.path.join(stanford_corenlp_path, 'slf4j-api-1.7.25.jar'),
            path_to_sihan_corpora_dict=os.path.join(stanford_corenlp_path, 'stanford-segmenter-2018-02-27', 'data'),
            path_to_model=os.path.join(stanford_corenlp_path, 'stanford-segmenter-2018-02-27', 'data', 'pku.gz'),
            path_to_dict=os.path.join(stanford_corenlp_path, 'stanford-segmenter-2018-02-27', 'data', 'dict-chris6.ser.gz'),
            sihan_post_processing='true'
        )

    def segment_sents(self, sentences):
        result = self.segmenter.segment_sents(sentences)
        result = result.strip()
        segmented_list = re.split(os.linesep, result)
        if len(segmented_list[-1]) == 0:
            segmented_list = segmented_list[:-1]
        print(len(segmented_list), len(sentences))
        assert len(segmented_list) == len(sentences)
        return segmented_list

    def tokenize(self, captions_for_images):
        image_id_list = []
        caption_list = []
        for (image_id, captions) in captions_for_images.items():
            for caption in captions:
                caption_list.append(caption['caption'])
                image_id_list.append(image_id)

        segmented_caption_list = self.segment_sents(caption_list)
        assert len(image_id_list) == len(caption_list) and len(caption_list) == len(segmented_caption_list)

        tokenized_captions_for_images = {}
        for i in range(len(image_id_list)):
            image_id = image_id_list[i]
            if image_id not in tokenized_captions_for_images:
                tokenized_captions_for_images[image_id] = []
            tokenized_captions_for_images[image_id].append(segmented_caption_list[i])
        return tokenized_captions_for_images


def evaluation(annotation_file, result_file):
    coco = COCO(annotation_file)
    cocoRes = coco.loadRes(result_file)
    # create cocoEval object by taking coco and cocoRes
    cocoEval = COCOEvalCap(coco, cocoRes, cls_tokenizer=StanfordTokenizer)

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
