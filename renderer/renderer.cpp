#define TO_INDEX(x, y, img) (((y)*img->xDim) + (x))
#define GET_X(idx, img) ((idx) % img->xDim)
#define GET_Y(idx, img) ((idx) / img->xDim)
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <vector>

extern "C" {

    typedef struct {
        int xDim;
        int yDim;
        int degree;
        int numPoly;
        double* coeffs;
        int* redRegion;
        int* greenRegion;
        int* blueRegion;
    } Image;

    int xShifts[] = {0, 0, 0, 0, 0, 0, 0};

    void setXShift(int curve, int shift) {
        xShifts[curve] = shift;
    }

    int evaluatePoly(int y, Image* img, int polyIdx) {
        double collector = 0.0;
        int currentDegree = img->degree;
        for (int i = 0; i < img->degree+1; i++) {
            double coeff = img->coeffs[(img->degree+1) * polyIdx + i];
            collector += coeff * pow(y, currentDegree);
            currentDegree--;
        }

        int toR = round(collector);
        toR += xShifts[polyIdx];
        return toR;
    }

    void renderToImage(Image* img, int* renderTo) {
        // evaluate each polynomial over the y-axis
        for (int y = 0; y < img->yDim; y++) {
            for (int polyIdx = 0; polyIdx < img->numPoly; polyIdx++) {
                int polyVal = evaluatePoly(y, img, polyIdx);
                int indexVal = TO_INDEX(polyVal, y, img);
                //printf("index to write to: x: %d, y: %d -> %d\n", polyVal, y, indexVal);
                renderTo[indexVal] = -1;
            }
        }
    }

    int labelNextRegion(Image* img, int* data, int regionLabel) {
        // scan the image left to right, then up and down
        int nextRegionIdx = -1;
        for (int i = 0; i < 520*504; i++) {
            if (data[i] == 0) {
                // found it
                nextRegionIdx = i;
            }
        }

        if (nextRegionIdx == -1)
            return 0; // couldn't find another region

        std::vector<int> queue;
        queue.push_back(nextRegionIdx);

        while (!queue.empty()) {
            int nextIdx = queue.back();
            queue.pop_back();
        
            if (data[nextIdx] != 0)
                continue;
        
            // if it isn't a 0, it is part of our region now.
            data[nextIdx] = regionLabel;

            // enqueue all of our neighbors
            int x = GET_X(nextIdx, img);
            int y = GET_Y(nextIdx, img);

            if (x - 1 >= 0) {
                queue.push_back(TO_INDEX(x-1, y, img));
            }
        
            if (x + 1 < img->xDim) {
                queue.push_back(TO_INDEX(x+1, y, img));
            }
        
            if (y - 1 >= 0) {
                queue.push_back(TO_INDEX(x, y-1, img));
            }
        
            if (y + 1 < img->yDim) {
                queue.push_back(TO_INDEX(x, y+1, img));
            }
        }

        return 1;
    }

    void makeChannel(int* labeledImg, int* channel,
                     int* colors, Image* img) {
        for (int i = 0; i < img->xDim * img->yDim; i++) {
            if (labeledImg[i] != -1) {
                channel[i] = colors[labeledImg[i]-1];
            }
        }

        for (int i = 0; i < img->xDim * img->yDim; i++) {
            if (labeledImg[i] == -1) {
                channel[i] = (channel[i-1] + channel[i+1]) / 2;
            }
        }
    }



    void getChannels(int* red, int* green, int* blue) {
        Image i;

        i.xDim = 504;
        i.yDim = 520;
        i.degree = 3;
        i.numPoly = 6;

        double coeffs[] = { 5.21077678e-07, 7.81409213e-04,-4.54538977e-01, 2.10766591e+02, 1.28745088e-07, 1.59508605e-03,-7.74351891e-01, 2.50757158e+02, -1.36611612e-06, 2.09329501e-03,-6.18243231e-01, 2.75820046e+02, 1.27859619e-06,-1.49002860e-04,-1.30547220e-01, 2.76185389e+02,-2.12685889e-06, 1.94450901e-03,-2.09131751e-01, 2.86335871e+02,1.52425141e-07, 6.48831267e-04,-1.24328052e-01, 3.22808640e+02 };


        int redRegion[] = { 65, 84, 241, 65, 84, 241, 65 };
        int greenRegion[] = { 86, 88, 241, 86, 88, 241, 86};
        int blueRegion[] = { 150, 92, 237, 150, 92, 237, 150};

        i.coeffs = coeffs;
        i.redRegion = redRegion;
        i.greenRegion = greenRegion;
        i.blueRegion = blueRegion;

        int result[520*504];

        for (int i = 0; i < 520*504; i++) {
            result[i] = 0;
        }

        renderToImage(&i, result);

        int regionIdx = 1;
        while (labelNextRegion(&i, result, regionIdx++) == 1);
        //int gotRegions = regionIdx - 1;

        makeChannel(result, red, redRegion, &i);
        makeChannel(result, green, greenRegion, &i);
        makeChannel(result, blue, blueRegion, &i);
    
  
    }


    int main(int argc, char** argv) {
        int dim = 520 * 504;
        int* red = (int*) calloc(sizeof(int), dim);
        int* green = (int*) calloc(sizeof(int), dim);
        int* blue = (int*) calloc(sizeof(int), dim);

        getChannels(red, green, blue);

        for (int i = 0; i < dim; i++)
            printf("%d,", green[i]);
    }

}


