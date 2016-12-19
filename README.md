# Art Amiss

A project for Codestellation Fall 2016, won best Artificial Intelligence Hack.

When humans look at abstract art, they get a sense that each work is composed of a series of shapes, curves, lines, or general objects. We also have an intuition about how those objects would move if they pushed, pulled, or otherwise manipulated, even though we've never seen an abstract painting move before. Our project focused on teaching computers the unspoken and intuitive shared experience of imagining interacting with abstract art. We also investigated what happened when we made art move in a precisely unintuitive way.

1. First, we use KMeans and marching cubes in order to evaluate noisy counters for the image.
2. Next, we smooth the counters via L1-regularized curve fitting and LASO regression.
3. Next, we use region growing algorithms to section off our image into distinct color zones.
4. Finally, we build a k-NN bitmap projection of the image. It looks like the original, but it is interactive!
5. The resulting render is composed of curves that can be intuitively manipulated with shifts, stretches, and rotations.
6. In order to create anti-intuitive manipulations, we use the Fourier phase shift principle in order to change the often-assumed and rarely-modified phase space of the frequency domain.

Some screenshots on [the devpost](https://devpost.com/software/art-amiss).
