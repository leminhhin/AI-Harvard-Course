# Lecture6 Language
## Tokenization
- Tách câu thành các n-grams (cụm nhỏ gồm n từ)
- Vì AI có thể không thấy cả câu bao giờ, nhưng có thể đã thấy qua từng từ

## Markov model
Tokenize thành các n-grams rồi dùng markov model dự đoán từ tiếp theo

## bag-of-words model
- use to classify text
- apply Naive Bayes

### Laplace smoothing
- Vấn đề: có từ không bao giờ xuất hiện => không apply naive bayes được
- Giải quyết: thêm 1 occurence cho mỗi từ trong dataset

## Information retrieval
- ranking words in document -> tf-idf (term frequency * inverse document frequency)

## Information extraction

## Word representation
word2vec