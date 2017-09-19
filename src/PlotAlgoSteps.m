    function PlotAlgoSteps()


    fileName = '~/Downloads/stepcounter_1505740246677';

    Data = csvread([fileName '-1-Data.csv']);
    Pre = csvread([fileName '-2-Pre.csv']);
    Smooth = csvread([fileName '-3-Smooth.csv']);
    PeakScore = csvread([fileName '-4-PeakScore.csv']);
    Peak = csvread([fileName '-5-Peak.csv']);
    ConfPeak = csvread([fileName '-6-ConfPeak.csv']);



    timeSlice = [60000 63000];

    Data = CropData(Data, timeSlice);
    Pre = CropData(Pre, timeSlice);
    Smooth = CropData(Smooth, timeSlice);
    PeakScore = CropData(PeakScore, timeSlice);
    Peak = CropData(Peak, timeSlice);
    ConfPeak = CropData(ConfPeak, timeSlice);
    

    index = 1;
%     subplot(2,3,index);
%     index = index + 1;
% 
%     plot(Data(:,1), ...
%         sqrt(Data(:,2).*Data(:,2) + ...
%              Data(:,3).*Data(:,3) + ...
%              Data(:,4).*Data(:,4)));
%     legend({'Acc magnitude'});

    figure(1);
    subplot(3,1,index);
    index = index + 1;
    plot(Pre(:,1), Pre(:,2), 'LineWidth', 3, 'Color', [0.8 0.8 0.8]);
    hold on;
    plot(Smooth(:,1), Smooth(:,2), 'k');
    lgd = legend({'Preprocessed', 'Filtered'}, 'Orientation', 'horizontal', 'Location', 'south');
    lgd.FontSize = 14;
    set(gca,'xtick',[])
    set(gca,'fontsize',14)
    set(gca,'xtick',[])


    subplot(3,1,index);
    index = index + 1;
    plot(PeakScore(:,1), PeakScore(:,2), 'r');
    lgd = legend({'Scored'}, 'Location', 'south');
    lgd.FontSize = 14;
    set(gca,'fontsize',14)
    set(gca,'xtick',[])


    subplot(3,1,index);
    index = index + 1;
    plot(Smooth(:,1), Smooth(:,2), 'k');
    hold on;
    plot(Peak(:,1), Peak(:,2), '.', 'MarkerSize',14);
    plot(ConfPeak(:,1), ConfPeak(:,2), 'o', 'MarkerSize',14);
    lgd = legend({'Filtered','Detection','Postprocessed'}, 'Orientation', 'horizontal', 'Location', 'south');
    lgd.FontSize = 14;
    set(gca,'fontsize',14)

end


function CroppedData = CropData(Data, TimeSlice)
    CroppedData = Data(Data(:,1) > TimeSlice(1) &  Data(:,1) < TimeSlice(2), :);
end



