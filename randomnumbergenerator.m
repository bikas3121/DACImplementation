% Reference Signal
nob = 16;
t = 0:1:2^nob+10;
rng('default')     % seed for the reproducibility of the random number
s = rng;

% generates the unifromly distributed INL between the given range
% r = a + (b-a).*rand(N,1).  % generate random number between given range
% Change the value of a and b to generate the INL with different LSB
% variates. 

INL =  0 + (4+0)*rand(length(t),1);   
INL = round(INL,2);

% figure()
% plot(1:1:length(INL), INL)
%% Quantizer Set
% plot(t,re)

writematrix(INL, 'INL.txt')
