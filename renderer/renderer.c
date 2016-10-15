#define TO_INDEX(x, y, img) ((y*img->xDim) + x)
#include <math.h>
#include <stdio.h>

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


int evaluatePoly(int y, Image* img, int polyIdx) {
    double collector = 0.0;
    int currentDegree = img->degree;
    for (int i = 0; i < img->degree+1; i++) {
        double coeff = img->coeffs[(img->degree+1) * polyIdx + i];

        /*printf("%f * (%d)^%d = %f\n",
               coeff,
               y,
               currentDegree,
               pow(y, currentDegree));*/
        collector += coeff * pow(y, currentDegree);
        currentDegree--;
    }

    int toR = round(collector);
    //if (polyIdx == 0)
    //    printf("Result: %d\n", toR);
    return toR;
}

void renderToImage(Image* img, int* renderTo) {
    // evaluate each polynomial over the y-axis
    for (int y = 0; y < img->yDim; y++) {
        for (int polyIdx = 0; polyIdx < img->numPoly; polyIdx++) {
            int polyVal = evaluatePoly(y, img, polyIdx);
            int indexVal = TO_INDEX(polyVal, y, img);
            //printf("index to write to: x: %d, y: %d -> %d\n", polyVal, y, indexVal);
            renderTo[indexVal] = 1;
        }
    }
}


int main(int argc, char** argv) {
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

    for (int i = 0; i < 520*504; i++) {
        printf("%d,", result[i]);
    }
    printf("\n");
}



