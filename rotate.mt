# Переставить первый символ в конец слова в алфавите a,b,c 
# Имена состояний в этой программе произвольные
# Начальным состоянием считается то, что встретилось в первом правиле
start,a->keepA,_,R
start,b->keepB,_,R
start,c->keepC,_,R
keepA,a->keepA,a,R
keepA,b->keepA,b,R
keepA,c->keepA,c,R
keepB,a->keepB,a,R
keepB,b->keepB,b,R
keepB,c->keepB,c,R
keepC,a->keepC,a,R
keepC,b->keepC,b,R
keepC,c->keepC,c,R
keepA,_->q0,a,N
keepB,_->q0,b,N
keepC,_->q0,c,N
