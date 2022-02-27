# spam
python3 cuenta_palabras.py test_input/spam.txt
diff test_input/spam_stats.txt test_true/spam_stats.txt
python3 cuenta_palabras.py -l test_input/spam.txt
diff test_input/spam_l_stats.txt test_true/spam_l_stats.txt
python3 cuenta_palabras.py -l test_input/spam.txt -b
diff test_input/spam_lb_stats.txt test_true/spam_lb_stats.txt
python3 cuenta_palabras.py -ls test_input/stopwords_en.txt test_input/spam.txt -b
diff test_input/spam_lsb_stats.txt test_true/spam_lsb_stats.txt
python3 cuenta_palabras.py -ls test_input/stopwords_en.txt test_input/spam.txt -bf
diff test_input/spam_lsbf_stats.txt test_true/spam_lsbf_stats.txt
python3 cuenta_palabras.py -s test_input/stopwords_en.txt test_input/spam.txt -bf
diff test_input/spam_sbf_stats.txt test_true/spam_sbf_stats.txt
# tirantloblanc
python3 cuenta_palabras.py test_input/tirantloblanc.txt -b
diff test_input/tirantloblanc_b_stats.txt test_true/tirantloblanc_b_stats.txt
python3 cuenta_palabras.py -l test_input/tirantloblanc.txt -b
diff test_input/tirantloblanc_lb_stats.txt test_true/tirantloblanc_lb_stats.txt
python3 cuenta_palabras.py -ls test_input/stopwords_en.txt test_input/tirantloblanc.txt -b
diff test_input/tirantloblanc_lsb_stats.txt test_true/tirantloblanc_lsb_stats.txt
python3 cuenta_palabras.py -ls test_input/stopwords_en.txt test_input/tirantloblanc.txt -bf
diff test_input/tirantloblanc_lsbf_stats.txt test_true/tirantloblanc_lsbf_stats.txt
# quijote
python3 cuenta_palabras.py -l test_input/quijote.txt -b
diff test_input/quijote_lb_stats.txt test_true/quijote_lb_stats.txt
python3 cuenta_palabras.py -ls test_input/stopwords_es.txt test_input/quijote.txt -b
diff test_input/quijote_lsb_stats.txt test_true/quijote_lsb_stats.txt
python3 cuenta_palabras.py -ls test_input/stopwords_es.txt test_input/quijote.txt -bf
diff test_input/quijote_lsbf_stats.txt test_true/quijote_lsbf_stats.txt
python3 cuenta_palabras.py -s test_input/stopwords_es.txt test_input/quijote.txt -b
diff test_input/quijote_sb_stats.txt test_true/quijote_sb_stats.txt