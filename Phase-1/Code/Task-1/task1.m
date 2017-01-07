% The user should choose r in such a way that it divides the frame into
% equal sized blocks that means r should be a common factor of frame height
% and width.
% n should be choosen as a power of 2
% as r decreases computation time increases

clearvars %clear the workspace
myDir = input('Give the full folder path for video files: ','s');
out_file = input('Give the name for output file: ','s');
r = input('Input for r: ');
n = input('Input for n in power of 2 and no more than 256: ');
%myDir = 'C:\Users\sphinx\Desktop\DataR';
%files = dir('C:\Users\sphinx\Desktop\DataR\*.mp4');
files = dir(strcat(myDir,'\*.mp4'));
t = numel(files);
totalCount = 0;
%fd = fopen('C:\Users\sphinx\Desktop\results.txt','w');
for k = 1:numel(files)
    filename = fullfile(myDir,files(k).name);
    %read the frames of the current video file into video
    v = VideoReader(filename);
    c=0;
    while hasFrame(v)
    readFrame(v);   
    c=c+1;
    end
    v1=VideoReader(filename); 
    %video = readFrame(v);
    %[a,b,c] = size(video);
    %frame = zeros(a,b);
    %c = v.NumberOfFrames;
    %for j = 1:c
    j=0;
    while hasFrame(v1)
        disp('my bad');
        %extract each frame
        frame = readFrame(v1);
        [fh,fw] = size(frame);
        j=j+1;
        frameGray = rgb2gray(frame);
        rowArg = zeros(1,r);
        colArg = zeros(1,r);
        [fh,fw] = size(frameGray);
        height = floor(fh/r);
        width = floor(fw/r);
            
        remH = rem(fh,r);
        remW = rem(fw,r);
        for y = 1:r
            if(y==r)
               rowArg(1,y) = height+remH;
               colArg(1,y) = width+remW;
            else
               rowArg(1,y) = height;
               colArg(1,y) = width;
            end
        end
        
        %divide frame into 40*40 blocks or cells
        cells = mat2cell(frameGray,rowArg,colArg);
        [m,p] = size(cells);
        if ~exist('mycell','var')
            disp('hi')
            mycell = cell(t*c*m*p,2);
        end
        count = 0;
        for u = 1:m
            for v = 1:p
                totalCount = totalCount+1;
                count = count+1;
                %take each cell and compute the color histogram%
                [counts,binLocations] = imhist(cells{u,v},n);
                %mycell{totalCount,1} = strcat(num2str(k),';',num2str(j),';',num2str(count));
                prefix = strcat(num2str(k),';',num2str(j),';',num2str(count));
                countT = counts';
                suffix = '';
                for e = 1:n
                    suffix = strcat(suffix,num2str(countT(1,e)),',');
                end
                finalStr = strcat(prefix,'>>',suffix);
                mycell{totalCount,1} = finalStr;
                imhist(cells{u,v},n);
                %mycell{totalCount,2} = counts';
            end
        end
    end
    %disp(size(video));
end
%xlswrite('C:\Users\sphinx\Desktop\tabledata.xls',mycell);
xlswrite(strcat(myDir,'\',out_file,'.xls'),mycell);
%fd = fopen('C:\Users\sphinx\Desktop\results.txt','w');
%fprintf(fd,'%s %s\r\n',mycell{:});
%fclose(fd);
