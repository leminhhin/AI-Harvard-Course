# Lecture3 Optimization

## Local search

Mục tiêu: Tìm state có cost thấp nhất (cao nhất)

Cost function: đánh giá chi phí

Bài toán: TSP, đặt vị trí bệnh viện sao cho gần nhà dân nhất

### Hill climbing

#### Steepest-ascent (choose best neighbor)

Đi đến neighbor có cost tốt nhất, nếu không có -> dừng

#### Stochastic

 Choose random from better neighbors

#### First choice

Choose first higher neighbor

#### Random restart

Hill climbing nhiều lần với initial state ngẫu nhiên

#### Local beam search

### Simulated annealing

Mục tiêu: thoát khỏi local minimum, local maximum

Ý tưởng: early on -> nhiều khả năng sẽ chấp nhận đi đến 1 state tệ hơn, later on -> khả năng giảm

## Linear programming

Bài toán: optimize production cost

Step 1: mô hình hóa cost function

Step 2: scipy.optimize.linprog()

## Constraint Satisfaction

Bài toán: xếp lịch, sudoku, tô màu bản đồ

Xem bên AI course của HCMUS

