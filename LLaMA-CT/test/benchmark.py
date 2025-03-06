import json
from rouge_score import rouge_scorer
from nltk.translate import meteor_score
import nltk
from collections import defaultdict
import numpy as np
from typing import List, Dict

# 下载必要的nltk数据
nltk.download('wordnet')
nltk.download('omw-1.4')

def compute_cider_score(refs: List[str], hyps: List[str]) -> float:
    def preprocess_sentence(sentence: str) -> List[str]:
        if not isinstance(sentence, str):
            sentence = str(sentence)
        return sentence.strip().lower().split()
    
    def compute_ngrams(words: List[str], n: int) -> Dict[tuple, int]:
        ngrams = defaultdict(int)
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i+n])
            ngrams[ngram] += 1
        return ngrams
    
    def compute_doc_frequency(refs_tokens: List[List[str]]) -> Dict[tuple, int]:
        doc_freq = defaultdict(int)
        for ref in refs_tokens:
            unigrams = compute_ngrams(ref, 1)
            for ngram in unigrams:
                doc_freq[ngram] += 1
        return doc_freq
    
    def compute_cider_score_single(ref_tokens: List[str], hyp_tokens: List[str], doc_freq: Dict[tuple, int], log_ref_len: float) -> float:
        if not ref_tokens or not hyp_tokens:
            return 0.0
            
        ref_ngrams = compute_ngrams(ref_tokens, 1)
        hyp_ngrams = compute_ngrams(hyp_tokens, 1)
        
        if not ref_ngrams or not hyp_ngrams:
            return 0.0
        
        all_ngrams = set(ref_ngrams.keys()) | set(hyp_ngrams.keys())
        if not all_ngrams:
            return 0.0
            
        vec_ref = []
        vec_hyp = []
        
        for ngram in all_ngrams:
            ref_count = ref_ngrams[ngram]
            hyp_count = hyp_ngrams[ngram]
            
            df = max(1, doc_freq[ngram])
            idf = max(0, log_ref_len - np.log(df))
            
            vec_ref.append(ref_count * idf)
            vec_hyp.append(hyp_count * idf)
        
        vec_ref = np.array(vec_ref)
        vec_hyp = np.array(vec_hyp)
        
        norm_ref = np.linalg.norm(vec_ref)
        norm_hyp = np.linalg.norm(vec_hyp)
        
        if norm_ref < 1e-8 or norm_hyp < 1e-8:
            return 0.0
        
        cosine_sim = np.dot(vec_ref, vec_hyp) / (norm_ref * norm_hyp)
        return max(-1.0, min(1.0, cosine_sim))
    
    valid_pairs = [(r, h) for r, h in zip(refs, hyps) if r and h]
    if not valid_pairs:
        return 0.0
        
    refs_tokens = [preprocess_sentence(ref) for ref, _ in valid_pairs]
    hyps_tokens = [preprocess_sentence(hyp) for _, hyp in valid_pairs]
    
    doc_freq = compute_doc_frequency(refs_tokens)
    num_refs = max(1, len(refs_tokens))
    log_ref_len = np.log(float(num_refs))
    
    scores = []
    for ref_tokens, hyp_tokens in zip(refs_tokens, hyps_tokens):
        score = compute_cider_score_single(ref_tokens, hyp_tokens, doc_freq, log_ref_len)
        if not np.isnan(score):
            scores.append(score)
    
    if not scores:
        return 0.0
        
    return np.mean(scores) * 10.0

def evaluate_answers(data):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    
    original_answers = []
    model_answers = []
    rouge_l_scores = []
    meteor_scores = []
    
    print("\n样本数据检查:")
    for item in data:
        for qa_pair in item['qa_pairs']:
            original_answer = qa_pair['original_answer']
            model_answer = qa_pair['model_answer']
            
            print(f"\n原始答案: {original_answer}")
            print(f"模型答案: {model_answer}")
            
            rouge_scores = scorer.score(original_answer, model_answer)
            rouge_score = rouge_scores['rougeL'].fmeasure
            if not np.isnan(rouge_score):
                rouge_l_scores.append(rouge_score)
            
            try:
                meteor = meteor_score.meteor_score([original_answer.split()], model_answer.split())
                if not np.isnan(meteor):
                    meteor_scores.append(meteor)
            except:
                print(f"METEOR计算错误 - 原始: {original_answer}, 模型: {model_answer}")
            
            original_answers.append(original_answer)
            model_answers.append(model_answer)
    
    cider_score = compute_cider_score(original_answers, model_answers)
    
    avg_rouge_l = np.mean(rouge_l_scores) if rouge_l_scores else 0.0
    avg_meteor = np.mean(meteor_scores) if meteor_scores else 0.0
    
    return {
        'ROUGE-L': avg_rouge_l,
        'METEOR': avg_meteor,
        'CIDEr': cider_score
    }

def main():
    try:
        with open('test_results.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("开始评估...")
        scores = evaluate_answers(data)
        
        print("\n评估结果:")
        print(f"ROUGE-L: {scores['ROUGE-L']:.4f}")
        print(f"METEOR: {scores['METEOR']:.4f}")
        print(f"CIDEr: {scores['CIDEr']:.4f}")
        
    except FileNotFoundError:
        print("错误：找不到 test_results.json 文件")
    except json.JSONDecodeError:
        print("错误：JSON 文件格式不正确")
    except Exception as e:
        print(f"发生错误：{str(e)}")

if __name__ == "__main__":
    main()