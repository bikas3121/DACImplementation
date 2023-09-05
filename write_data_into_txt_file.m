%
data = readmatrix('simulationresult.csv');

t = data(:,1);  % simulation time samples

ref_filt = data(:,2);   % filtered reference signal

u_mpc2_filt = data(:,6); % optimally quantized reference signal with non-unifrom quantizer without INL feedback

u_mpcINL_filt = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback


writematrix(t, 'OutputData/samplingtime.txt')
writematrix(ref_filt, 'OutputData/filtered_reference_signal.txt')
writematrix(u_mpc2_filt, 'OutputData/mpc_non_uniform_no_INL_feedback.txt')
writematrix(u_mpc2_filt, 'OutputData/mpc_non_uniform_wtih_INL_feedback.txt')