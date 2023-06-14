echo put 5 in index 1
curl -i -X PUT localhost:10000/op1 -d '5'

echo post calculate
curl -i -X POST localhost:10000/calculate

echo put 56 in index 2
curl -i -X PUT localhost:10000/op2 -d '56'

echo get 5 in index 1
curl -i -X GET localhost:10000/op1 -d '5'

echo get value from index 3
curl -i -X GET localhost:10000/op3

echo post calculate
curl -i -X POST localhost:10000/calculate

echo post calculate dot
curl -i -X POST localhost:10000/calculate -H Operand:'+'
