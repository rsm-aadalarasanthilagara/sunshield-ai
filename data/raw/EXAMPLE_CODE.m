clear;
close('all');

%%% parse variables
filename = '20250802_UCSD_Campus_Bike.txt'
M = load(filename);
Time = M(:,1);
LAT = M(:,2);
LONG = M(:,3);
ALT = M(:,4);
Temp = M(:,5);
RH = M(:,6);

%%% filter data with no GPS fix in San Diego
j = find(LAT < 32 | LAT > 34); 
Time(j,:) = NaN;
LAT(j,:) = NaN;
LONG(j,:) = NaN;
ALT(j,:) = NaN;
Temp(j,:) = NaN;
RH(j,:) = NaN;

%%% plot color-coded heat map (latitude, longtitude, temperature)
deltaT = [min(Temp), max(Temp)];  %% temperature range
cmap = colormap('jet');

%%% Date:  2 August --> local_time = GMT - 8  (Noon = 0.5)
local_time = Time - 8/24;  %%% subtract 8 hours from GMT time

%%% plot time series of temperature and relative humidity
figure('Position', [300  100  1280 720], "Color", "white");
subplot(2,1,1);
plot(local_time, Temp, '-r', 'LineWidth', 2);
ylabel('temperature (^{o}C');

subplot(2,1,2);
plot(local_time, RH, '-b', 'LineWidth', 2);
xlabel('local time (Day of Year)');
ylabel('relative humidity (%)');

%%% overlay color-coded heat map on satellite imagery
figure('Position', [300  100  1280 720], "Color", "white");
geobasemap satellite;
geoplot(LAT, LONG, '-r', 'LineWidth', 1);
[latlim longlim] = geolimits(gca);
set(gca,'NextPlot', 'add', 'FontSize', 14);

for(i = 1:length(Temp)-1)
     cc = round(((Temp(i))-(min(deltaT)))./((max(deltaT))-(min(deltaT))).*(length(cmap(:,1))-1))+1;  %%% color of segment
     if(cc > length(cmap(:,1))), cc = length(cmap(:,1)); end;
     if(cc < 1), cc = 1; end;
     geoplot(LAT(i:i+1), LONG(i:i+1), '-', 'Color', cmap(cc,:), 'LineWidth', 4);
end; 

colormap('jet');
c = colorbar(gca,"eastoutside");
c.Label.String = 'temperature (^{o}C)';
clim([deltaT]);

disp('Done');
