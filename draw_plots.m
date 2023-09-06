% plot simulation results from python 
% read data
data = readmatrix('filtered_simulationresult.csv'); 

t = data(:,1);  % simulation time samples

ref_filt = data(:,2);   % filtered reference signal

u_direct_filt = data(:,3);  % directly quantized reference signal with unifrom quantizer

u_directINL_filt = data(:,4);  % directly quantized reference signal with non-unifrom quantizer

u_mpc1_filt = data(:,5); % optimally quantized reference signal with unifrom quantizer without INL feedback

u_mpc2_filt = data(:,6); % optimally quantized reference signal with non-unifrom quantizer without INL feedback

u_mpcINL_filt = data(:,7); % optimally quantized reference signal with non-unifrom quantizer with INL feedback

%% Plots
figure()
plot(t, ref_filt)
hold on 
plot(t, u_direct_filt)
hold on 
plot(t,u_mpc1_filt)
hold on 
plot(t,u_mpc2_filt)
xlabel('Time')
% legend('Reference','Direct', 'Direct(INL)','MPC(Cf)', 'MPC(Cf) + INL','MPC', 'MPC(INL)')
legend('Reference','Direct', 'MPC + NO INL', 'MPC + INL')
grid minor

figure()
plot(t, ref_filt)
hold on 
plot(t, u_direct_filt)
hold on 
plot(t, u_directINL_filt)
hold on
plot(t,u_mpc1_filt)
hold on 
plot(t,u_mpc2_filt)
hold on 
plot(t,u_mpcINL_filt)
xlabel('Time')

legend('Reference','Direct', 'Direct(INL)', 'MPC Unifrom','MPC w/o INL feedback', 'MPC with INL feedback')
% legend('Reference','Direct', 'MPC (Closed-form)', 'MPC-Gurobi')
grid minor



%% error and variance
% 
% 
err_direct = ref_filt-u_direct_filt;
var_direct = var(err_direct);

err_directINL = ref_filt-u_directINL_filt;
var_directINL = var(err_directINL);
 
err_mpc1 = ref_filt - u_mpc1_filt;
var_mpc1 = var(err_mpc1);

err_mpc2 = ref_filt - u_mpc2_filt;
var_mpc2 = var(err_mpc2);
% 
err_mpcINL = ref_filt - u_mpcINL_filt;
var_mpcINL = var(err_mpcINL);

x = categorical({'Direct', 'MPC (Closed-form)'});
% x = categorical({'Direct(Ideal DAC)', 'Direct(Non-ideal DAC)', 'MPC(Ideal DAC)','MPC(Non-ideal DAC)','MPC(Non-ideal DAC)-F'});
% x = [1,2];
y = [round(var_direct,4) round(var_directINL,4);  round(var_mpc1,4) round(var_mpc2,4) ];
figure()
b = bar(x,y);
xtips1 = b(1).XEndPoints;
ytips1 = b(1).YEndPoints;
labels1 = string(b(1).YData);
text(xtips1,ytips1,labels1,'HorizontalAlignment','center','VerticalAlignment','bottom')

xtips2 = b(2).XEndPoints;
ytips2 = b(2).YEndPoints;
labels2 = string(b(2).YData);
text(xtips2,ytips2,labels2,'HorizontalAlignment','center','VerticalAlignment','bottom')
xtickangle(45)
ylabel('Error Variance')
% legend('Ideal DAC (Uniform)', 'Non-ideal DAC (INL)')
grid minor


%% 
% 
x1 = categorical({'Direct', 'MPC (Closed-form)', 'MPC-INL'});
% x = categorical({'Direct(Ideal DAC)', 'Direct(Non-ideal DAC)', 'MPC(Ideal DAC)','MPC(Non-ideal DAC)','MPC(Non-ideal DAC)-F'});
% x = [1,2];
y1 = [round(var_direct,4) round(var_directINL,4);  round(var_mpc1,4) round(var_mpc2,4);  round(var_mpc1,4) round(var_mpcINL,4) ];
figure()
b1 = bar(x1,y1);
xtips1 = b1(1).XEndPoints;
ytips1 = b1(1).YEndPoints;
labels1 = string(b1(1).YData);
text(xtips1,ytips1,labels1,'HorizontalAlignment','center','VerticalAlignment','bottom')

xtips2 = b1(2).XEndPoints;
ytips2 = b1(2).YEndPoints;
labels2 = string(b1(2).YData);
text(xtips2,ytips2,labels2,'HorizontalAlignment','center','VerticalAlignment','bottom')

% xtips3 = b1(3).XEndPoints;
% ytips3 = b1(3).YEndPoints;
% labels3 = string(b1(3).YData);
% text(xtips3,ytips3,labels3,'HorizontalAlignment','center','VerticalAlignment','bottom')

xtickangle(45)

ylabel('Error Variance')
% legend('Ideal DAC (Uniform)', 'Non-ideal DAC (INL)')
grid minor
