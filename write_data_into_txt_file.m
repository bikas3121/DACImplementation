%
%% Unfiltered data

data = readmatrix('unfiltered_simulationresult.csv');

% read data
t = data(:,1);  % simulation time samples
ref = data(:,2);   % filtered reference signal
u_mpc2 = data(:,6); % optimally quantized reference signal with non-unifrom quantizer without INL feedback
u_mpcINL = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback

% write data
writematrix(t, 'OutputData/Unfiltered/samplingtime.txt')
writematrix(ref_filt, 'OutputData/Unfiltered/reference_signal.txt')
writematrix(u_mpc2_filt, 'OutputData/Unfiltered/mpc_non_uniform_no_INL_feedback.txt')
writematrix(u_mpc2_filt, 'OutputData/Unfiltered/mpc_non_uniform_wtih_INL_feedback.txt')

%% Filterd data
data = readmatrix('simulationresult.csv');

%read data
t = data(:,1);  % simulation time samples
ref_filt = data(:,2);   % filtered reference signal
u_mpc2_filt = data(:,6); % optimally quantized reference signal with non-unifrom quantizer without INL feedback
u_mpcINL_filt = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback

% write
writematrix(t, 'OutputData/Filtered/samplingtime.txt')
writematrix(ref_filt, 'OutputData/Filtered/filtered_reference_signal.txt')
writematrix(u_mpc2_filt, 'OutputData/Filtered/mpc_non_uniform_no_INL_feedback.txt')
writematrix(u_mpc2_filt, 'OutputData/Filtered/mpc_non_uniform_wtih_INL_feedback.txt')




