# Переставить местами первый и последний символы слова в алфавите a,b
# Захват первого символа
q1,a->qa,a,R
q1,b->qb,b,R
# Переход на конец слова
qa,a->qa,a,R
qa,b->qa,b,R
qa,_->qe,_,L
qb,a->qb,a,R
qb,b->qb,b,R
qb,_->qf,_,L
# Запись символа и захват последнего
qe,a->qA,a,L
qe,b->qB,a,L
qf,a->qA,b,L
qf,b->qB,b,L
# Переход на начало слова
qA,a->qA,a,L
qA,b->qA,b,L
qA,_->qE,_,R
qB,a->qB,a,L
qB,b->qB,b,L
qB,_->qF,_,R
# Запись символа
qE,a->q0,a,n
qE,b->q0,a,n
qF,a->q0,b,n
qF,b->q0,b,n

