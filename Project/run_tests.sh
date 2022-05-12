# indexer & stats
python3 SAR_Indexer.py -M corpora/2015 2015_index_M.bin > test_stats_2015_M.txt
diff test_stats_2015_M.txt stats/stats_2015_M.txt

python3 SAR_Indexer.py -S corpora/2015 2015_index_S.bin > test_stats_2015_S.txt
diff test_stats_2015_S.txt stats/stats_2015_S.txt

python3 SAR_Indexer.py -S -P corpora/2015 2015_index_SP.bin > test_stats_2015_SP.txt
diff test_stats_2015_SP.txt stats/stats_2015_SP.txt

python3 SAR_Indexer.py -S -P -M corpora/2015 2015_index_SPM.bin > test_stats_2015_SPM.txt
diff test_stats_2015_SPM.txt stats/stats_2015_SPM.txt

python3 SAR_Indexer.py -S -P -M -O corpora/2015 2015_index_SPMO.bin > test_stats_2015_SPMO.txt
diff test_stats_2015_SPMO.txt stats/stats_2015_SPMO.txt

python3 SAR_Indexer.py -S -P -M -O corpora/2016 2016_index_SPMO.bin > test_stats_2016_SPMO.txt
diff test_stats_2016_SPMO.txt stats/stats_2016_SPMO.txt


# python3 SAR_Searcher.py -S -T results/result_2015_edited_stemming.txt 2015_index_SPMO.bin



# # indexer: stopwords, permuterm, multifield
# python3 SAR_Indexer.py -S -P -M -O corpora/2015 2015_index_full.bin
# python3 SAR_Indexer.py -S -P -M -O corpora/2016 2016_index_full.bin

# # searcher: minimo stemming
# python3 SAR_Searcher.py -S -T results/result_2015_minimo_stemming.txt 2015_index_full.bin
# python3 SAR_Searcher.py -S -T results/result_2016_minimo_stemming.txt 2016_index_full.bin
# # full stemming
# python3 SAR_Searcher.py -S -T results/result_2015_full_stemming.txt 2015_index_full.bin
# python3 SAR_Searcher.py -S -T results/result_2016_full_stemming.txt 2016_index_full.bin