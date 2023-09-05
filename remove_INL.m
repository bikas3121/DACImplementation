% remove INL from the data
data = readmatrix('unfiltered_simulationresult.csv');
INL = readmatrix('INL.txt');
INL(1) = 0;

% read data
t = data(:,1);  % simulation time samples
ref = data(:,2);   % filtered reference signal
u_direct = data(:,3);  % directly quantized reference signal with unifrom quantizer
u_mpc2 = data(:,5); % optimally quantized reference signal with non-unifrom quantizer without INL feedback
u_mpcINL = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback
u_mpc_trun = data(:,8); % optimally quantized reference signal with non-unifrom quantizer with INL feedback

% write data
writematrix(t, 'OutputData/Unfiltered/samplingtime.txt')
writematrix(ref, 'OutputData/Unfiltered/reference_signal.txt')
writematrix(u_direct, 'OutputData/Unfiltered/direct_quantized.txt')
writematrix(u_mpc2, 'OutputData/Unfiltered/mpc_without_INLfeedback.txt')
writematrix(u_mpcINL, 'OutputData/Unfiltered/mpc_with_INLfeedback.txt')
writematrix(u_mpc_trun, 'OutputData/Unfiltered/mpc_with_INLfeedback_truncated.txt')

%% Remove INL 
% Q = 0:1:max(ref);
% INL = INL(1:length(Q));
% INL_dict = dictionary(Q, INL');
% 
% u_mpc_trun = zeros(length(u_mpcINL),1);
% for i = 1:length(u_mpcINL)
%     u_i = u_mpcINL(i);
%     INL_i = INL_dict(floor(u_i));
%     u_mpc_trun(i) = u_i-INL_i;
% end
% 
% writematrix(u_mpc_trun, 'OutputData/Unfiltered/mpc_with_INLfeedback_truncated.txt')


%% Plots
lenu = length(u_mpcINL);

err_1 = u_mpc_trun- u_mpc2;
figure()
plot(1:1:lenu, err_1)
xlabel('Time')
grid on 


figure()
plot(1:1:lenu, u_mpc_trun);
hold on 
plot(1:1:lenu, u_mpcINL)
legend('trun', 'with INL')
xlabel('Time')
grid on 

