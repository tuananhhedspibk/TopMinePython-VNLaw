import phrase_lda
import sys
import utils

arguments = sys.argv

num_topics = int(arguments[1])
iteration = 1000
optimization_burnin = 100
alpha = 10
optimization_iterations = 50
beta = 0.5

print 'Running PhraseLDA...'

partitioned_docs = utils.load_partitioned_docs()
vocab_file = utils.load_vocab()

plda = phrase_lda.PhraseLDA( partitioned_docs, vocab_file, num_topics , alpha, beta, iteration, optimization_iterations, optimization_burnin)

document_phrase_topics, most_frequent_topics, docs_topic_info, topics = plda.run()

utils.store_phrase_topics(document_phrase_topics)
utils.store_most_frequent_topics(most_frequent_topics)
docs_topic_info_standard, documents_tp_ph_repre = utils.store_phrase_topics_pro(partitioned_docs, docs_topic_info, document_phrase_topics, vocab_file, num_topics, topics)

utils.compute_distance_between_articles(docs_topic_info_standard)
utils.vectorize_keyword_topics_distribution(topics, documents_tp_ph_repre, num_topics, vocab_file)
