%
%% Unfiltered data

data = readmatrix('unfiltered_simulationresult.csv');

% read data
t = data(:,1);  % simulation time samples
ref = data(:,2);   % filtered reference signal
u_direct = data(:,3);  % directly quantized reference signal with unifrom quantizer
u_mpc2 = data(:,6); % optimally quantized reference signal with non-unifrom quantizer without INL feedback
u_mpcINL = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback

% write data
writematrix(t, 'OutputData/Unfiltered/samplingtime.txt')
writematrix(ref, 'OutputData/Unfiltered/reference_signal.txt')
writematrix(u_direct, 'OutputData/Unfiltered/direct_quantized.txt')
writematrix(u_mpc2, 'OutputData/Unfiltered/mpc_non_uniform_no_INL_feedback.txt')
writematrix(u_mpcINL, 'OutputData/Unfiltered/mpc_non_uniform_wtih_INL_feedback.txt')


%% Rounded off values
u_direct_tr = round(u_direct);
u_mpc_tr = round(u_mpc2);
u_mpcINL_tr = round(u_mpcINL);
writematrix(t, 'OutputData/Truncated/samplingtime.txt')
writematrix(u_direct_tr, 'OutputData/Truncated/direct_quantized_truncated.txt')
writematrix(u_mpc_tr, 'OutputData/Truncated/mpc_noINLfeedback_quantized_truncated.txt')
writematrix(u_mpcINL_tr, 'OutputData/Truncated/mpc_withINLfeedback_quantized_truncated.txt')
%% Filterd data
data = readmatrix('simulationresult.csv');

%read data
t = data(:,1);  % simulation time samples
ref_filt = data(:,2);   % filtered reference signal
u_direct_filt = data(:,3);  % directly quantized reference signal with unifrom quantizer
u_mpc2_filt = data(:,6); % optimally quantized reference signal with non-unifrom quantizer without INL feedback
u_mpcINL_filt = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback

% write
writematrix(t, 'OutputData/Filtered/samplingtime.txt')
writematrix(ref_filt, 'OutputData/Filtered/filtered_reference_signal.txt')
writematrix(u_direct_filt, 'OutputData/Filtered/directquantized_signal.txt')
writematrix(u_mpc2_filt, 'OutputData/Filtered/mpc_non_uniform_no_INL_feedback.txt')
writematrix(u_mpcINL_filt, 'OutputData/Filtered/mpc_non_uniform_wtih_INL_feedback.txt')







