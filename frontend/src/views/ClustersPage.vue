<template>
  <div class="min-h-screen bg-[#FFF4EA] flex">
    <!-- ========== LEFT STICKY TABLE OF CONTENTS ========== -->
    <aside class="sticky top-20 w-1/6 h-screen border-r p-4 bg-[#FFF4EA] flex-shrink-0 overflow-y-auto">
      <h2 class="text-xl font-bold mb-4">Table of Contents</h2>
      <nav class="flex flex-col space-y-2">
        <a href="#pca-driven-analysis" class="text-black-500 hover:underline">
          I. PCA Driven Analysis
        </a>
        <a href="#other-dr-analysis" class="text-black-500 hover:underline">
          II. Other DR Techniques
        </a>
      </nav>
    </aside>

    <!-- ========== MAIN CONTENT AREA ========== -->
    <div class="flex-1 p-6">
      <!-- ~~~~~ SECTION I: PCA DRIVEN ANALYSIS ~~~~~ -->
      <section id="pca-driven-analysis" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">I. PCA Driven Analysis (Curated)</h1>
        <p class="text-sm mb-4 text-gray-600">
          This section displays results from a curated clustering approach. Data is first reduced using Principal Component Analysis (PCA)
          to a target explained variance. Various clustering algorithms are then applied to this PCA-reduced data.
          The resulting clusters are visualized using a selected dimensionality reduction technique (e.g., UMAP, t-SNE), and detailed characteristics
          (ratings distributions, category compositions, prominent notes) are shown for each significant cluster identified.
        </p>

        <!-- ========== PART 1: PCA OVERVIEW (Variance, Loadings, Generic Curated Viz) ========== -->
        <div class="mb-6 pb-6 border-b">
          <h2 class="text-xl font-semibold mb-4">1. PCA Overview & General Visualizations</h2>
          <p class="text-xs mb-2 text-gray-500">Fetches PCA variance, loadings, and general curated visualizations for all clustering algorithms (using a default DR for visualization like UMAP).</p>
          <div class="flex flex-wrap gap-x-4 gap-y-4 items-end">
            <div class="flex flex-col w-full sm:w-32">
              <label for="pcaDecade" class="text-sm font-medium">Decade</label>
              <v-select
                id="pcaDecade"
                :options="availableDecades"
                v-model="filters.pcaAnalysis.decade"
                class="mt-1 bg-white"
                :clearable="false"
              />
            </div>
            <div class="flex flex-col w-full sm:w-32">
              <label for="pcaGender" class="text-sm font-medium">Gender</label>
              <v-select
                id="pcaGender"
                :options="availableGenders"
                v-model="filters.pcaAnalysis.gender"
                class="mt-1 bg-white"
                :clearable="false"
              />
            </div>
            <div>
              <button @click="fetchPcaAnalysis" :disabled="loadingPcaOverview" class="bg-[#C96868] text-white py-2 px-4 rounded-md hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]">
                {{ loadingPcaOverview ? "Loading Overview..." : "Get PCA Overview" }}
              </button>
            </div>
          </div>
           <!-- Error Message for PCA Overview -->
          <p v-if="errorPcaOverview" class="mt-4 text-red-600 font-medium text-center">
            {{ errorPcaOverview }}
          </p>
          <!-- Display Area for PCA Overview Images -->
          <div v-if="images.pcaOverview.length > 0" class="mt-6 flex justify-center h-96 overflow-y-auto items-start">
            <ul class="space-y-8 w-full max-w-4xl">
              <li v-for="(group, groupIndex) in images.pcaOverview" :key="'pca-overview-' + group.filename + '-' + groupIndex" class="border-b pb-6 mb-6">
                <h3 class="text-lg font-semibold mb-3 text-center">{{ group.title }}</h3>
                <div class="relative flex justify-center items-stretch">
                  <div class="flex-shrink-0 max-w-[70%]">
                    <img :src="'data:image/png;base64,' + group.base64" :alt="group.title" class="w-full h-auto rounded-md shadow-md object-contain"/>
                  </div>
<!--                  <div class="relative pl-2 transition-all duration-1000" :class="[expandedIndicesPcaOverview.includes(groupIndex) ? 'w-80' : 'w-24']">-->
<!--                    <div class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"-->
<!--                         @click="toggleExplanation(groupIndex, expandedIndicesPcaOverview, displayedTextPcaOverview, textToDisplayPca.overview, images.pcaOverview)">-->
<!--                      {{ expandedIndicesPcaOverview.includes(groupIndex) ? 'Hide Info' : 'More Info' }}-->
<!--                    </div>-->
<!--                    <transition name="fade">-->
<!--                      <div v-if="expandedIndicesPcaOverview.includes(groupIndex)" class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2 max-h-96 overflow-y-auto">-->
<!--                        <h4 class="font-bold mb-2">Explanation</h4>-->
<!--                        <p class="text-sm whitespace-pre-wrap">{{ displayedTextPcaOverview[groupIndex] }}</p>-->
<!--                      </div>-->
<!--                    </transition>-->
<!--                  </div>-->
                </div>
              </li>
            </ul>
          </div>
          <p v-else-if="attemptedFetchPcaOverview && !loadingPcaOverview" class="mt-6 text-gray-500 text-center">
              No PCA Overview images found for the selected filters.
          </p>
        </div>


        <!-- ========== PART 2: CURATED CLUSTER DETAILS ========== -->
        <div class="mb-6 pb-6 border-b">
            <h2 class="text-xl font-semibold mb-4">2. View Specific Curated Cluster Details</h2>
            <p class="text-xs mb-2 text-gray-500">
              Uses the Decade/Gender from below. Select a clustering algorithm (applied after PCA) and a method to visualize these clusters in 2D.
              This will show an overall 2D visualization, and then a carousel detailing characteristics (violin, pie, histograms) and perfumes for each cluster.
            </p>
            <!-- Filter Inputs -->
            <div class="flex flex-wrap gap-x-4 gap-y-4 items-end mb-6">
                <div class="flex flex-col w-full sm:w-32">
                  <label for="pcaAdditionalDecade" class="text-sm font-medium">Decade</label>
                  <v-select
                    id="pcaAdditionalDecade"
                    :options="availableDecades"
                    v-model="filters.pcaAdditionalAnalysis.decade"
                    class="mt-1 bg-white"
                    :clearable="false"
                  />
                </div>
                <div class="flex flex-col w-full sm:w-32">
                  <label for="pcaAdditionalGender" class="text-sm font-medium">Gender</label>
                  <v-select
                    id="pcaAdditionalGender"
                    :options="availableGenders"
                    v-model="filters.pcaAdditionalAnalysis.gender"
                    class="mt-1 bg-white"
                    :clearable="false"
                  />
                </div>
                <div class="flex flex-col w-full sm:w-60">
                    <label for="curatedClusteringMethod" class="text-sm font-medium">Clustering Algorithm</label>
                    <v-select id="curatedClusteringMethod" :options="availableCuratedClusteringMethods" v-model="selectedCuratedClusteringMethod" placeholder="Select Algorithm" class="mt-1 bg-white" :clearable="false"></v-select>
                </div>
                <div class="flex flex-col w-full sm:w-60">
                    <label for="curatedDrMethod" class="text-sm font-medium">Visualization DR Method</label>
                    <v-select id="curatedDrMethod" :options="availableCuratedDrMethods" v-model="selectedCuratedDrMethod" placeholder="Select DR Method" class="mt-1 bg-white" :clearable="false"></v-select>
                </div>
                <div>
                    <button @click="fetchCuratedClusterDetails" :disabled="loadingCuratedDetails || !selectedCuratedClusteringMethod || !selectedCuratedDrMethod" class="bg-[#C96868] text-white py-2 px-4 rounded-md hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]">
                        {{ loadingCuratedDetails ? "Loading Details..." : "Get Cluster Details" }}
                    </button>
                </div>
            </div>
            <p v-if="errorCuratedDetails" class="mt-4 text-red-600 font-medium text-center">
                {{ errorCuratedDetails }}
            </p>

            <!-- WRAPPER FOR SCROLLABLE CONTENT + SIDE NAVIGATION BUTTONS -->
            <div class="relative part2-outer-wrapper">

                <!-- SCROLLABLE CONTENT AREA -->
                <div class="part2-scrollable-content" style="max-height: 80vh; overflow-y: auto; padding: 0 15px;">
                    <!-- Overall 2D Visualization -->
                    <div v-if="curatedOverviewVisualization" class="mb-8 flex justify-center items-start pt-4">
                        <div class="w-full max-w-3xl mx-auto">
                            <h3 class="text-lg font-semibold mb-3 text-center">{{ curatedOverviewVisualization.title || 'Overall Cluster Visualization' }}</h3>
                            <div class="relative flex justify-center items-stretch">
                                <div class="flex-shrink-0 w-full h-full">
                                    <img :src="'data:image/png;base64,' + curatedOverviewVisualization.base64" :alt="curatedOverviewVisualization.title || 'Overall Visualization'" class="w-full h-auto rounded-md shadow-md object-contain"/>
                                </div>
<!--                                <div class="relative pl-2 transition-all duration-1000" :class="[expandedCuratedOverviewViz ? 'w-80' : 'w-24']">-->
<!--                                    <div class="sticky top-4 z-20 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"-->
<!--                                         @click="toggleCuratedOverviewExplanation()">-->
<!--                                        {{ expandedCuratedOverviewViz ? 'Hide Info' : 'More Info' }}-->
<!--                                    </div>-->
<!--                                    <transition name="fade">-->
<!--                                        <div v-if="expandedCuratedOverviewViz" class="sticky top-16 z-20 bg-white p-4 shadow-md rounded mt-2 max-h-96 overflow-y-auto">-->
<!--                                            <h4 class="font-bold mb-2">Explanation</h4>-->
<!--                                            <p class="text-sm whitespace-pre-wrap">{{ textCuratedOverviewViz }}</p>-->
<!--                                        </div>-->
<!--                                    </transition>-->
<!--                                </div>-->
                            </div>
                        </div>
                    </div>

                    <!-- Carousel for Individual Clusters -->
                    <div v-if="curatedClustersDisplayData.length > 0" class="w-full max-w-3xl mx-auto">
                        <Carousel ref="curatedCarouselRef" v-bind="carouselConfigCurated" @slide-end="onCuratedCarouselSlideEnd">
                            <Slide v-for="(cluster, slideIndex) in curatedClustersDisplayData" :key="'curated-slide-' + cluster.clusterLabel + '-' + slideIndex">
                                <div class="p-4 w-full">
                                    <h3 class="text-xl font-bold mb-4 text-center">Cluster {{ cluster.clusterLabel }} Details</h3>
                                    <!-- Cluster Specific Images -->
                                    <div class="mb-6">
                                        <h4 class="text-lg font-semibold mb-3 text-center">Cluster Visualizations</h4>
                                        <ul class="space-y-8">
                                            <li v-for="(imageItem, imageIndex) in cluster.images" :key="'curated-clusterimg-' + slideIndex + '-' + imageIndex" class="border-b pb-6 mb-6">
                                                <h5 class="text-md font-semibold mb-2 text-center">{{ imageItem.title || 'Cluster Image' }}</h5>
                                                <div class="relative flex justify-center items-stretch">
                                                    <div class="flex-shrink-0 max-w-[70%]">
                                                        <img :src="'data:image/png;base64,' + imageItem.base64" :alt="imageItem.title" class="w-full h-auto rounded-md shadow-md object-contain"/>
                                                    </div>
<!--                                                    <div class="relative pl-2 transition-all duration-1000" :class="[isCuratedImageExpanded(slideIndex, imageIndex) ? 'w-80' : 'w-24']">-->
<!--                                                        <div class="sticky top-4 z-20 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"-->
<!--                                                            @click="toggleCuratedItemExplanation(slideIndex, imageIndex, imageItem.title)">-->
<!--                                                            {{ isCuratedImageExpanded(slideIndex, imageIndex) ? 'Hide Info' : 'More Info' }}-->
<!--                                                        </div>-->
<!--                                                        <transition name="fade">-->
<!--                                                            <div v-if="isCuratedImageExpanded(slideIndex, imageIndex)" class="sticky top-16 z-20 bg-white p-4 shadow-md rounded mt-2 max-h-80 overflow-y-auto">-->
<!--                                                                <h6 class="font-bold mb-1">Explanation</h6>-->
<!--                                                                <p class="text-xs whitespace-pre-wrap">{{ getCuratedImageText(slideIndex, imageIndex) }}</p>-->
<!--                                                            </div>-->
<!--                                                        </transition>-->
<!--                                                    </div>-->
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                    <!-- Perfumes in Cluster -->
                                    <div>
                                        <h4 class="text-lg font-semibold mb-3 text-center">Perfumes in this Cluster ({{ cluster.perfumes.length }})</h4>
                                        <div v-if="cluster.perfumes.length > 0"
                                             class="perfumes-scroll-container bg-gray-50 p-2 rounded-md"
                                             style="max-height: 400px; overflow-y: auto;">
                                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                                <a v-for="(perfume, pIndex) in cluster.perfumes" :key="'cluster-' + cluster.clusterLabel + '-perfume-' + pIndex"
                                                   :href="perfume.link" target="_blank" class="block bg-white shadow rounded p-4 hover:shadow-lg transition-shadow">
                                                    <img v-if="perfume.image" :src="perfume.image" alt="Perfume" class="w-full h-48 object-cover rounded-t-md mb-2"/>
                                                    <div v-else class="w-full h-48 bg-gray-200 rounded-t-md mb-2 flex items-center justify-center text-gray-400">No Image</div>
                                                    <h5 class="font-semibold text-md mb-1 truncate" :title="perfume.name">{{ perfume.name || 'Perfume Details' }}</h5>
                                                    <p class="text-gray-600 text-xs_NO_FONT_SIZES_HERE mb-2 h-16 overflow-y-auto">{{ perfume.description || 'No description available.' }}</p>
                                                    <span class="text-xs text-blue-500 hover:underline">View Product</span>
                                                </a>
                                            </div>
                                        </div>
                                        <p v-else class="text-gray-500 text-center">No perfumes listed for this cluster.</p>
                                    </div>
                                </div>
                            </Slide>
                            <template #addons>
                                <Pagination />
                            </template>
                        </Carousel>
                    </div>
                </div>

                <!-- Custom Navigation Buttons - OUTSIDE the scrollable area, INSIDE the relative wrapper -->
                <template v-if="curatedClustersDisplayData.length > 1">
                    <button @click="curatedCarouselPrev"
                            class="custom-side-nav custom-side-nav-prev"
                            title="Previous Cluster" aria-label="View Previous Cluster">
                        &lt;
                    </button>
                    <button @click="curatedCarouselNext"
                            class="custom-side-nav custom-side-nav-next"
                            title="Next Cluster" aria-label="View Next Cluster">
                        &gt;
                    </button>
                </template>

            </div>
            <p v-if="attemptedFetchCuratedDetails && !loadingCuratedDetails && !curatedOverviewVisualization" class="mt-6 text-gray-500 text-center">
                No Curated Cluster Detail images or data found for the selected algorithm and DR method.
            </p>
        </div>
      </section>

      <!-- ~~~~~ SECTION II: OTHER DIMENSIONALITY REDUCTION TECHNIQUES ~~~~~ -->
      <section id="other-dr-analysis" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">II. Other Dimensionality Reduction Techniques (2D Direct)</h1>
        <p class="text-sm mb-4 text-gray-600">
        This section explores clustering results when dimensionality reduction (DR) techniques are applied to reduce data directly to 2D.
        Various clustering algorithms are then run on this 2D data.
        The 2D DR plot with cluster labels is shown, along with detailed characteristics for each significant cluster.
        Note: the current version of the platform supports UMAP direct reduction only, as the results of other DR methods might not be suitable for clusterization. Although the use of UMAP is also a bit unorthodox in such pipelines, there is some research that backs up this approach.<sup class="text-xs">[1,2]</sup>
        </p>

        <!-- References section -->
        <div class="mt-6 pt-4 border-t border-gray-200">
          <h4 class="text-sm font-semibold text-gray-700 mb-2">References</h4>
          <div class="text-xs text-gray-600 space-y-1">
            <p>[1] Considerably Improving Clustering Algorithms Using UMAP Dimensionality Reduction Technique: A Comparative Study. ResearchGate.
               <a href="https://www.researchgate.net/publication/340388772_Considerably_Improving_Clustering_Algorithms_Using_UMAP_Dimensionality_Reduction_Technique_A_Comparative_Study"
                  class="text-blue-600 hover:text-blue-800 underline break-all"
                  target="_blank"
                  rel="noopener noreferrer">
                 https://www.researchgate.net/publication/340388772_Considerably_Improving_Clustering_Algorithms_Using_UMAP_Dimensionality_Reduction_Technique_A_Comparative_Study
               </a>
            </p>
            <p>[2] UMAP Documentation - Clustering.
               <a href="https://umap-learn.readthedocs.io/en/latest/clustering.html"
                  class="text-blue-600 hover:text-blue-800 underline"
                  target="_blank"
                  rel="noopener noreferrer">
                 https://umap-learn.readthedocs.io/en/latest/clustering.html
               </a>
            </p>
          </div>
        </div>
        <div class="mt-6 pt-4 mb-6 flex flex-col border-t items-start">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>
          <div class="flex flex-wrap gap-x-4 gap-y-4 items-end">
            <div class="flex flex-col w-full sm:w-32">
              <label for="otherDrDecade" class="text-sm font-medium">Decade</label>
              <v-select
                id="otherDrDecade"
                :options="availableDecades"
                v-model="filters.otherDrAnalysis.decade"
                class="mt-1 bg-white"
                :clearable="false"
              />
            </div>
            <div class="flex flex-col w-full sm:w-32">
              <label for="otherDrGender" class="text-sm font-medium">Gender</label>
              <v-select
                id="otherDrGender"
                :options="availableGenders"
                v-model="filters.otherDrAnalysis.gender"
                class="mt-1 bg-white"
                :clearable="false"
              />
            </div>
            <div class="flex flex-col w-full sm:w-60">
                    <label for="allClusteringMethod" class="text-sm font-medium">Clustering Algorithm</label>
                    <v-select id="allClusteringMethod" :options="availableCuratedClusteringMethods" v-model="selectedAllClusteringMethod" placeholder="Select Algorithm" class="mt-1 bg-white" :clearable="false"></v-select>
            </div>
            <div class="flex flex-col w-full sm:w-60">
                    <label for="allDrMethod" class="text-sm font-medium">DR Method</label>
                    <v-select id="allDrMethod" :options="availableOtherDrMethods" v-model="selectedAllDrMethod" placeholder="Select DR Method" class="mt-1 bg-white" :clearable="false"></v-select>
            </div>
            <div>
              <button @click="fetchOtherDrAnalysis" :disabled="loadingOtherDr || !selectedAllClusteringMethod || !selectedAllDrMethod" class="bg-[#C96868] text-white py-2 px-4 rounded-md hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]">
                {{ loadingOtherDr ? "Loading..." : "Get " + selectedDrMethodDisplay + " Analysis" }}
              </button>
            </div>
          </div>
        </div>
        <p v-if="errorOtherDr" class="mt-4 text-red-600 font-medium text-center">{{ errorOtherDr }}</p>
        <!-- SCROLLABLE CONTENT AREA -->
        <div class="relative part2-outer-wrapper">
          <div class="part2-scrollable-content" style="max-height: 80vh; overflow-y: auto; padding: 0 15px;">
              <!-- Overall 2D Visualization -->
              <div v-if="otherDrOverviewVisualization" class="mb-8 flex justify-center items-start pt-4">
                  <div class="w-full max-w-3xl mx-auto">
                      <h3 class="text-lg font-semibold mb-3 text-center">{{ otherDrOverviewVisualization.title || 'Overall Cluster Visualization' }}</h3>
                      <div class="relative flex justify-center items-stretch">
                          <div class="flex-shrink-0 w-full h-full">
                              <img :src="'data:image/png;base64,' + otherDrOverviewVisualization.base64" :alt="otherDrOverviewVisualization.title || 'Overall Visualization'" class="w-full h-auto rounded-md shadow-md object-contain"/>
                          </div>
  <!--                        <div class="relative pl-2 transition-all duration-1000" :class="[expandedOtherDrOverviewViz ? 'w-80' : 'w-24']">-->
  <!--                            <div class="sticky top-4 z-20 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"-->
  <!--                                 @click="toggleOtherDrOverviewExplanation()">-->
  <!--                                {{ expandedOtherDrOverviewViz ? 'Hide Info' : 'More Info' }}-->
  <!--                            </div>-->
  <!--                            <transition name="fade">-->
  <!--                                <div v-if="expandedOtherDrOverviewViz" class="sticky top-16 z-20 bg-white p-4 shadow-md rounded mt-2 max-h-96 overflow-y-auto">-->
  <!--                                    <h4 class="font-bold mb-2">Explanation</h4>-->
  <!--                                    <p class="text-sm whitespace-pre-wrap">{{ textOtherDrOverviewViz }}</p>-->
  <!--                                </div>-->
  <!--                            </transition>-->
  <!--                        </div>-->
                      </div>
                  </div>
              </div>

              <!-- Carousel for Individual Clusters -->
              <div v-if="otherDrClustersDisplayData.length > 0" class="w-full max-w-3xl mx-auto">
                  <Carousel ref="otherDrCarouselRef" v-bind="carouselConfigOtherDr" @slide-end="onOtherDrCarouselSlideEnd">
                      <Slide v-for="(cluster, slideIndex) in otherDrClustersDisplayData" :key="'otherdr-slide-' + cluster.clusterLabel + '-' + slideIndex">
                          <div class="p-4 w-full">
                              <h3 class="text-xl font-bold mb-4 text-center">Cluster {{ cluster.clusterLabel }} Details</h3>
                              <!-- Cluster Specific Images -->
                              <div class="mb-6">
                                  <h4 class="text-lg font-semibold mb-3 text-center">Cluster Visualizations</h4>
                                  <ul class="space-y-8">
                                      <li v-for="(imageItem, imageIndex) in cluster.images" :key="'otherdr-clusterimg-' + slideIndex + '-' + imageIndex" class="border-b pb-6 mb-6">
                                          <h5 class="text-md font-semibold mb-2 text-center">{{ imageItem.title || 'Cluster Image' }}</h5>
                                          <div class="relative flex justify-center items-stretch">
                                              <div class="flex-shrink-0 max-w-[70%]">
                                                  <img :src="'data:image/png;base64,' + imageItem.base64" :alt="imageItem.title" class="w-full h-auto rounded-md shadow-md object-contain"/>
                                              </div>
  <!--                                            <div class="relative pl-2 transition-all duration-1000" :class="[isOtherDrImageExpanded(slideIndex, imageIndex) ? 'w-80' : 'w-24']">-->
  <!--                                                <div class="sticky top-4 z-20 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"-->
  <!--                                                    @click="toggleOtherDrItemExplanation(slideIndex, imageIndex, imageItem.title)">-->
  <!--                                                    {{ isOtherDrImageExpanded(slideIndex, imageIndex) ? 'Hide Info' : 'More Info' }}-->
  <!--                                                </div>-->
  <!--                                                <transition name="fade">-->
  <!--                                                    <div v-if="isOtherDrImageExpanded(slideIndex, imageIndex)" class="sticky top-16 z-20 bg-white p-4 shadow-md rounded mt-2 max-h-80 overflow-y-auto">-->
  <!--                                                        <h6 class="font-bold mb-1">Explanation</h6>-->
  <!--                                                        <p class="text-xs whitespace-pre-wrap">{{ getOtherDrImageText(slideIndex, imageIndex) }}</p>-->
  <!--                                                    </div>-->
  <!--                                                </transition>-->
  <!--                                            </div>-->
                                          </div>
                                      </li>
                                  </ul>
                              </div>
                              <!-- Perfumes in Cluster -->
                              <div>
                                  <h4 class="text-lg font-semibold mb-3 text-center">Perfumes in this Cluster ({{ cluster.perfumes.length }})</h4>
                                  <div v-if="cluster.perfumes.length > 0"
                                       class="perfumes-scroll-container bg-gray-50 p-2 rounded-md"
                                       style="max-height: 400px; overflow-y: auto;">
                                      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                          <a v-for="(perfume, pIndex) in cluster.perfumes" :key="'otherdr-cluster-' + cluster.clusterLabel + '-perfume-' + pIndex"
                                             :href="perfume.link" target="_blank" class="block bg-white shadow rounded p-4 hover:shadow-lg transition-shadow">
                                              <img v-if="perfume.image" :src="perfume.image" alt="Perfume" class="w-full h-48 object-cover rounded-t-md mb-2"/>
                                              <div v-else class="w-full h-48 bg-gray-200 rounded-t-md mb-2 flex items-center justify-center text-gray-400">No Image</div>
                                              <h5 class="font-semibold text-md mb-1 truncate" :title="perfume.name">{{ perfume.name || 'Perfume Details' }}</h5>
                                              <p class="text-gray-600 text-xs_NO_FONT_SIZES_HERE mb-2 h-16 overflow-y-auto">{{ perfume.description || 'No description available.' }}</p>
                                              <span class="text-xs text-blue-500 hover:underline">View Product</span>
                                          </a>
                                      </div>
                                  </div>
                                  <p v-else class="text-gray-500 text-center">No perfumes listed for this cluster.</p>
                              </div>
                          </div>
                      </Slide>
                      <template #addons>
                          <Pagination />
                      </template>
                  </Carousel>
              </div>
          </div>

          <!-- Custom Navigation Buttons - OUTSIDE the scrollable area, INSIDE the relative wrapper -->
          <template v-if="otherDrClustersDisplayData.length > 1">
              <button @click="otherDrCarouselPrev"
                      class="custom-side-nav custom-side-nav-prev"
                      title="Previous Cluster" aria-label="View Previous Cluster">
                  &lt;
              </button>
              <button @click="otherDrCarouselNext"
                      class="custom-side-nav custom-side-nav-next"
                      title="Next Cluster" aria-label="View Next Cluster">
                  &gt;
              </button>
          </template>
        </div>
        <p v-if="!loadingOtherDr && attemptedFetchOtherDr && !otherDrOverviewVisualization" class="mt-6 text-gray-500 text-center">
            No {{selectedDrMethodDisplay}} analysis images found for the selected filters.
        </p>

      </section>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";
import 'vue3-carousel/carousel.css'
import { Carousel, Slide, Pagination } from 'vue3-carousel' // Removed Navigation as we use custom

const carouselGlobalConfig = {
  itemsToShow: 1.0,
  wrapAround: false,
  breakpointMode: 'carousel'
};

export default {
  name: "ClusteringAnalysis",
  components: {
    vSelect,
    Carousel,
    Slide,
    Pagination,
    // Navigation, // Removed
  },
  data() {
    return {
      carouselConfigCurated: { ...carouselGlobalConfig },
      availableCuratedClusteringMethods: [
          {label: "KMeans", value: "KMeans"},
          {label: "Affinity Propagation", value: "AffinityPropagation"},
          {label: "Agglomerative", value: "Agglomerative"},
          {label: "DBSCAN", value: "DBSCAN"},
          {label: "HDBSCAN", value: "HDBSCAN"},
          {label: "Gaussian Mixture", value: "GaussianMixture"},
          {label: "Spectral Clustering", value: "SpectralClustering"},
      ],
      availableCuratedDrMethods: [
          {label: "t-SNE", value: "tsne"},
          {label: "UMAP", value: "umap"},
          {label: "LLE", value: "lle"},
          {label: "Isomap", value: "isomap"},
      ],
      availableOtherDrMethods: [
          // {label: "t-SNE", value: "tsne"},
          {label: "UMAP", value: "umap"}
          // {label: "LLE", value: "lle"},
          // {label: "Isomap", value: "isomap"},
      ],
      availableDecades: [
        { label: "All", value: "All" },
        // { label: "1990s", value: "1990" },
        // { label: "2000s", value: "2000" },
        // { label: "2010s", value: "2010" },
        // { label: "2020s", value: "2020" },
      ],
      availableGenders: [
        { label: "All", value: "All" },
        { label: "Masculine", value: "Masculine" },
        { label: "Feminine", value: "Feminine" },
      ],
      selectedCuratedClusteringMethod: null,
      selectedAllClusteringMethod: null,
      selectedAllDrMethod: null,
      selectedCuratedDrMethod: null,

      otherDrOverviewVisualization: null,
      otherDrClustersDisplayData: [],

      expandedOtherDrOverviewViz: false,
      textOtherDrOverviewViz: "",

      expandedOtherDrItemExplanationState: {},
      textOtherDrItemExplanationState: {},

      loadingPcaOverview: false,
      loadingCuratedDetails: false,
      loadingOtherDr: false,

      errorPcaOverview: "",
      errorCuratedDetails: "",
      errorOtherDr: "",

      attemptedFetchPcaOverview: false,
      attemptedFetchCuratedDetails: false,
      attemptedFetchOtherDr: false,

      filters: {
        pcaAnalysis: { decade: { label: "All", value: "All" }, gender: { label: "All", value: "All" } },
        pcaAdditionalAnalysis: { decade: { label: "All", value: "All" }, gender: { label: "All", value: "All" } },
        otherDrAnalysis: { decade: { label: "All", value: "All" }, gender: { label: "All", value: "All" }},
      },
      images: {
        pcaOverview: [],
        otherDrAnalysis: [],
      },

      curatedOverviewVisualization: null,
      curatedClustersDisplayData: [],

      expandedCuratedOverviewViz: false,
      textCuratedOverviewViz: "",

      expandedCuratedItemExplanationState: {},
      textCuratedItemExplanationState: {},

      drMethods: [
          { name: "UMAP", value: "umap"},
          { name: "t-SNE", value: "tsne"},
          { name: "LLE", value: "lle"},
          { name: "Isomap", value: "isomap"}
      ],

      textToDisplayPca: {
        overview: {
            DEFAULT: "General explanation for PCA overview plots. These illustrate initial PCA results like variance explained and feature contributions.",
            PCA_VARIANCE: "This plot shows the percentage of dataset variance captured by each principal component (PC) and the cumulative variance. It helps determine how many PCs are needed to represent most of the data's information.",
            PCA_LOADINGS: "PCA loadings indicate how much each original feature contributes to a principal component. Larger absolute values mean a stronger influence of that feature on the PC. This helps interpret what each PC represents.",
            GENERAL_CURATED_VIZ: "This is a general 2D visualization (e.g., UMAP or t-SNE) of the data after initial PCA reduction, showing an overview of clusters found by various algorithms."
        },
        details: {
            DEFAULT: "Detailed explanation for this visualization.",
            CURATED_ALGO_VIZ: "This is a 2D visualization (using the selected DR method like UMAP or t-SNE) of the data *after initial PCA reduction*, with points colored by clusters found by the *selected clustering algorithm*. It helps assess cluster separation for this specific algorithm.",
            CLUSTER_RATINGS_VIOLIN: "Violin plots show the distribution of user ratings (e.g., scent, longevity) for perfumes within this specific cluster. The shape indicates data density, and comparison across clusters can reveal distinct preferences.",
            CLUSTER_CATEGORIES_PIE: "Pie charts display the average composition of fragrance categories (e.g., Type, Style, Season, Occasion) for perfumes within this cluster. 'Others' typically groups categories with small percentages. This highlights the dominant fragrance profiles of the cluster.",
            CLUSTER_NOTES_HISTOGRAM: "This histogram shows the frequency of the top fragrance notes for perfumes belonging to this specific cluster, highlighting its dominant scent characteristics and ingredients."
        }
      },
      displayedTextPcaOverview: [],
      expandedIndicesPcaOverview: [],

      textToDisplayOtherDr: {
          DEFAULT: "General explanation for plots from other DR techniques. These plots show results when data is directly reduced to 2D using the selected method, followed by clustering.",
          DR_VIZ: "A 2D scatter plot of the data reduced by the selected non-PCA method (e.g., UMAP, t-SNE). Points are colored by clusters found by a subsequent algorithm (like KMeans or DBSCAN), showing cluster structure in this specific 2D representation.",
          CLUSTER_RATINGS_VIOLIN: "Violin plots for this cluster show user rating distributions (scent, longevity, etc.). Comparing these across clusters found via this DR method can highlight unique perceived qualities.",
          CLUSTER_CATEGORIES_PIE: "Category composition pie charts for this cluster, revealing its typical fragrance types (e.g., predominantly Oriental or Fresh) as identified through this DR and clustering pathway.",
          CLUSTER_NOTES_HISTOGRAM: "Top notes histogram for this cluster, indicating its key scent ingredients and olfactory profile based on this specific DR and clustering result."
      },
      displayedTextOtherDr: [],
      expandedIndicesOtherDr: [],
    };
  },
  computed: {
    selectedDrMethodDisplay() {
      const selected = this.drMethods.find(m => m.value === this.filters.otherDrAnalysis.drMethod);
      return selected ? selected.name : 'DR';
    },
  },
  methods: {
    // Other DR Overview explanation toggle
    toggleOtherDrOverviewExplanation() {
      this.expandedOtherDrOverviewViz = !this.expandedOtherDrOverviewViz;
      if (this.expandedOtherDrOverviewViz) {
        const title = this.otherDrOverviewVisualization?.title || 'Overall Cluster Visualization';
        const explanation = this.getExplanationText(title, this.textToDisplayOtherDr);
        this.typeTextSimple('textOtherDrOverviewViz', explanation);
      } else {
        this.textOtherDrOverviewViz = "";
      }
    },

    // Other DR item expansion methods
    isOtherDrImageExpanded(slideIndex, imageIndex) {
      const key = `otherdr_${slideIndex}_${imageIndex}`;
      return !!this.expandedOtherDrItemExplanationState[key];
    },

    getOtherDrImageText(slideIndex, imageIndex) {
      const key = `otherdr_${slideIndex}_${imageIndex}`;
      return this.textOtherDrItemExplanationState[key] || "";
    },

    toggleOtherDrItemExplanation(slideIndex, imageIndex, imageTitle) {
      const key = `otherdr_${slideIndex}_${imageIndex}`;
      const isCurrentlyExpanded = this.isOtherDrImageExpanded(slideIndex, imageIndex);
      this.expandedOtherDrItemExplanationState[key] = !isCurrentlyExpanded;

      if (!isCurrentlyExpanded) {
        const explanation = this.getExplanationText(imageTitle, this.textToDisplayOtherDr);
        this.typeTextWithKey(this.textOtherDrItemExplanationState, key, explanation);
      } else {
        this.textOtherDrItemExplanationState[key] = "";
      }
    },

    // Other DR carousel navigation
    otherDrCarouselPrev() {
      this.$refs.otherDrCarouselRef?.prev();
    },

    otherDrCarouselNext() {
      this.$refs.otherDrCarouselRef?.next();
    },

    getExplanationText(imageTitle, textMapForSection) {
        if (!imageTitle || !textMapForSection) return textMapForSection?.DEFAULT || "No explanation available.";
        const titleLower = imageTitle.toLowerCase();

        if (textMapForSection === this.textToDisplayPca.overview) {
            if (titleLower.includes("explained variance")) return textMapForSection.PCA_VARIANCE;
            if (titleLower.includes("loadings")) return textMapForSection.PCA_LOADINGS;
            if (titleLower.includes("curated") && titleLower.includes("all_clustering_algos")) return textMapForSection.GENERAL_CURATED_VIZ;
        }

        if (textMapForSection === this.textToDisplayPca.details) {
            if (titleLower.includes("ratings violin") || titleLower.includes("violin plots")) return textMapForSection.CLUSTER_RATINGS_VIOLIN;
            if (titleLower.includes("categories pie") || titleLower.includes("avg categories piecharts")) return textMapForSection.CLUSTER_CATEGORIES_PIE;
            if (titleLower.includes("notes histogram")) return textMapForSection.CLUSTER_NOTES_HISTOGRAM;
            if (titleLower.includes("overall cluster visualization") || (this.selectedCuratedDrMethod && titleLower.includes(this.selectedCuratedDrMethod.value) && this.selectedCuratedClusteringMethod && titleLower.includes(this.selectedCuratedClusteringMethod.value.toLowerCase()) ) ) return textMapForSection.CURATED_ALGO_VIZ;
        }

        if (textMapForSection === this.textToDisplayOtherDr) {
            if (titleLower.includes("ratings violin") || titleLower.includes("violin plots")) return textMapForSection.CLUSTER_RATINGS_VIOLIN;
            if (titleLower.includes("categories pie") || titleLower.includes("avg categories piecharts")) return textMapForSection.CLUSTER_CATEGORIES_PIE;
            if (titleLower.includes("notes histogram")) return textMapForSection.CLUSTER_NOTES_HISTOGRAM;
            if (titleLower.includes("2d visualization") || titleLower.includes("umap") || titleLower.includes("tsne") || titleLower.includes("lle") || titleLower.includes("isomap")) return textMapForSection.DR_VIZ;
        }
      return textMapForSection?.DEFAULT || "Explanation details not found for this image.";
    },

    typeTextWithKey(targetTextObject, key, textToDisplayForThisImage) {
        let currentCharacterIndex = 0;
        targetTextObject[key] = "";
        const interval = setInterval(() => {
            if (currentCharacterIndex < textToDisplayForThisImage.length) {
            targetTextObject[key] += textToDisplayForThisImage[currentCharacterIndex];
            currentCharacterIndex++;
            } else {
            clearInterval(interval);
            }
        }, 15);
    },

    typeTextSimple(targetDataProperty, textToDisplayForThisImage) {
        let currentCharacterIndex = 0;
        this[targetDataProperty] = "";
        const interval = setInterval(() => {
            if (currentCharacterIndex < textToDisplayForThisImage.length) {
            this[targetDataProperty] += textToDisplayForThisImage[currentCharacterIndex];
            currentCharacterIndex++;
            } else {
            clearInterval(interval);
            }
        }, 15);
    },

    toggleExplanation(index, expandedIndicesArray, displayedTextArray, sourceTextMapForSection, currentImageList) {
      const i = expandedIndicesArray.indexOf(index);
      const imageTitle = currentImageList[index]?.title || "";
      if (i > -1) {
        expandedIndicesArray.splice(i, 1);
        displayedTextArray[index] = "";
      } else {
        expandedIndicesArray.push(index);
        const specificExplanation = this.getExplanationText(imageTitle, sourceTextMapForSection);
        let currentCharacterIndex = 0;
        displayedTextArray[index] = "";
        const interval = setInterval(() => {
          if (currentCharacterIndex < specificExplanation.length) {
            displayedTextArray[index] += specificExplanation[currentCharacterIndex];
            currentCharacterIndex++;
          } else {
            clearInterval(interval);
          }
        }, 15);
      }
    },

    toggleCuratedOverviewExplanation() {
        this.expandedCuratedOverviewViz = !this.expandedCuratedOverviewViz;
        if (this.expandedCuratedOverviewViz) {
            const title = this.curatedOverviewVisualization?.title || 'Overall Cluster Visualization';
            const explanation = this.getExplanationText(title, this.textToDisplayPca.details);
            this.typeTextSimple('textCuratedOverviewViz', explanation);
        } else {
            this.textCuratedOverviewViz = "";
        }
    },

    isCuratedImageExpanded(slideIndex, imageIndex) {
        const key = `${slideIndex}_${imageIndex}`;
        return !!this.expandedCuratedItemExplanationState[key];
    },
    getCuratedImageText(slideIndex, imageIndex) {
        const key = `${slideIndex}_${imageIndex}`;
        return this.textCuratedItemExplanationState[key] || "";
    },
    toggleCuratedItemExplanation(slideIndex, imageIndex, imageTitle) {
        const key = `${slideIndex}_${imageIndex}`;
        const isCurrentlyExpanded = this.isCuratedImageExpanded(slideIndex, imageIndex);
        this.expandedCuratedItemExplanationState[key] = !isCurrentlyExpanded;

        if (!isCurrentlyExpanded) {
            const explanation = this.getExplanationText(imageTitle, this.textToDisplayPca.details);
            this.typeTextWithKey(this.textCuratedItemExplanationState, key, explanation);
        } else {
            this.textCuratedItemExplanationState[key] = "";
        }
    },
    curatedCarouselPrev() {
      this.$refs.curatedCarouselRef?.prev();
    },
    curatedCarouselNext() {
      this.$refs.curatedCarouselRef?.next();
    },

    async fetchPcaAnalysis() {
      this.loadingPcaOverview = true;
      this.errorPcaOverview = "";
      this.attemptedFetchPcaOverview = true;
      this.images.pcaOverview = [];
      this.expandedIndicesPcaOverview = [];
      this.displayedTextPcaOverview = [];

      try {
        const params = {
          gender: this.filters.pcaAnalysis.gender.value,
          decade: this.filters.pcaAnalysis.decade.value
        }
        const response = await apiClient.get("/test/clustering-pca-analysis", {params});
        this.images.pcaOverview = response.data.images || [];
        if (this.images.pcaOverview.length > 0) {
          this.displayedTextPcaOverview = Array(this.images.pcaOverview.length).fill("");
        }
      } catch (err) {
        this.errorPcaOverview = err.response?.data?.error || "Failed to fetch PCA overview data.";
        this.images.pcaOverview = [];
      } finally {
        this.loadingPcaOverview = false;
      }
    },

    async fetchCuratedClusterDetails() {
      if (!this.selectedCuratedClusteringMethod || !this.selectedCuratedDrMethod) {
        this.errorCuratedDetails = "Please select both a clustering algorithm and a visualization DR method.";
        return;
      }
      this.loadingCuratedDetails = true;
      this.errorCuratedDetails = "";
      this.attemptedFetchCuratedDetails = true;
      this.curatedOverviewVisualization = null;
      this.curatedClustersDisplayData = [];
      this.expandedCuratedOverviewViz = false;
      this.textCuratedOverviewViz = "";
      this.expandedCuratedItemExplanationState = {};
      this.textCuratedItemExplanationState = {};
      try {
        const params = {
          decade: this.filters.pcaAdditionalAnalysis.decade.value,
          gender: this.filters.pcaAdditionalAnalysis.gender.value,
          clustering_method: this.selectedCuratedClusteringMethod.value,
          dr_method: this.selectedCuratedDrMethod.value
        };
        const response = await apiClient.get("/test/clustering-curated-cluster-details/", {params});
        this.curatedOverviewVisualization = response.data.overviewVisualization || null;
        this.curatedClustersDisplayData = response.data.clustersData || [];
      } catch (err) {
        this.errorCuratedDetails = err.response?.data?.error || `Failed to fetch details for ${this.selectedCuratedClusteringMethod.label} with ${this.selectedCuratedDrMethod.label} visualization.`;
        this.curatedOverviewVisualization = null;
        this.curatedClustersDisplayData = [];
      } finally {
        this.loadingCuratedDetails = false;
      }
    },

    async fetchOtherDrAnalysis() {
    if (!this.selectedAllClusteringMethod || !this.selectedAllDrMethod) {
      this.errorOtherDr = "Please select both a clustering algorithm and a visualization DR method.";
      return;
    }

    this.loadingOtherDr = true;
    this.errorOtherDr = "";
    this.attemptedFetchOtherDr = true;
    this.images.otherDrAnalysis = [];
    this.expandedIndicesOtherDr = [];
    this.displayedTextOtherDr = [];

    // Reset Other DR specific data
    this.otherDrOverviewVisualization = null;
    this.otherDrClustersDisplayData = [];
    this.expandedOtherDrOverviewViz = false;
    this.textOtherDrOverviewViz = "";
    this.expandedOtherDrItemExplanationState = {};
    this.textOtherDrItemExplanationState = {};

    try {
      const params = {
        decade: this.filters.otherDrAnalysis.decade.value,
        gender: this.filters.otherDrAnalysis.gender.value,
        clustering_method: this.selectedAllClusteringMethod.value,
        dr_method: this.selectedAllDrMethod.value
      };

      const response = await apiClient.get("/test/clustering-other-dr-analysis", { params });

      // Assuming the API returns similar structure to curated analysis
      this.otherDrOverviewVisualization = response.data.overviewVisualization || null;
      this.otherDrClustersDisplayData = response.data.clustersData || [];

      // Keep the old images array for backward compatibility if needed
      this.images.otherDrAnalysis = response.data.images || [];
      if (this.images.otherDrAnalysis.length > 0) {
        this.displayedTextOtherDr = Array(this.images.otherDrAnalysis.length).fill("");
      }
    } catch (err) {
      this.errorOtherDr = err.response?.data?.error || `Failed to fetch ${this.selectedDrMethodDisplay} analysis data.`;
      this.images.otherDrAnalysis = [];
      this.otherDrOverviewVisualization = null;
      this.otherDrClustersDisplayData = [];
    } finally {
      this.loadingOtherDr = false;
    }
  },
  },
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
aside {
  min-height: 100vh;
}
.whitespace-pre-wrap {
  white-space: pre-wrap;
}

/* v-select styling */
/*
:deep(.vs__dropdown-toggle) {
  border-radius: 0.375rem; border: 1px solid #D1D5DB; padding: 0.375rem 0.75rem; min-height: 2.5rem;
}
:deep(.vs__selected-options) { padding: 0; }
:deep(.vs__selected) { margin: 0; padding: 0.125rem 0; font-size: 0.875rem; color: #1F2937; }
:deep(.vs__search) { font-size: 0.875rem; padding: 0.125rem 0; }
:deep(.vs__actions .vs__clear), :deep(.vs__actions .vs__open-indicator) { fill: #6B7280; transform: scale(0.8); }
:deep(.vs__dropdown-menu) {
  border-color: #D1D5DB; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  max-height: 220px;
  overflow-y: auto;
}
:deep(.vs__dropdown-option) { padding: 0.5rem 0.75rem; font-size: 0.875rem; }
:deep(.vs__dropdown-option--highlight) { background-color: #E0A9A9; color: white; }
*/

/* Part 2: Curated Cluster Details - Outer Wrapper and Scrollable Content */
.part2-outer-wrapper {
  position: relative;
  padding-left: 60px;  /* Space for left button */
  padding-right: 60px; /* Space for right button */
}

.part2-scrollable-content {
  /* max-height and overflow-y are set inline in the template */
  /* e.g., style="max-height: 80vh; overflow-y: auto; padding: 0 15px;" */
}

/* Custom Side Navigation Buttons for Part 2 Carousel */
.custom-side-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 30;
  background-color: rgba(201, 104, 104, 0.8);
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
}
.custom-side-nav:hover {
  background-color: #C96868;
  transform: translateY(-50%) scale(1.05);
}
.custom-side-nav-prev {
  left: 5px; /* Position within the left padding of .part2-outer-wrapper */
}
.custom-side-nav-next {
  right: 5px; /* Position within the right padding of .part2-outer-wrapper */
}

/* Sticky "More Info" buttons within Part 2's scrollable content */
/* These 'top' values are relative to the .part2-scrollable-content div */
.part2-scrollable-content .sticky.top-4 { top: 4px; }
.part2-scrollable-content .sticky.top-16 { top: 52px; /* Approx button height + top offset + margin */ }
/* Note: The original .sticky.top-20 and .sticky.top-32 were for Part 1, keep them as they are if Part 1 is not scrollable in this way. */
/* If Part 1 "More Info" also needs adjustment due to a scroll container, apply similar logic. */


/* Default vue3-carousel pagination styling */
:deep(.carousel__pagination-button--active) {
  background-color: #C96868 !important;
}
:deep(.carousel__pagination-button) {
  background-color: #FADFA1;
}

/* Scrollbar for internal perfume list (within each carousel slide) */
.perfumes-scroll-container::-webkit-scrollbar {
  width: 8px;
}
.perfumes-scroll-container::-webkit-scrollbar-track {
  background: #f1f1f1; border-radius: 10px;
}
.perfumes-scroll-container::-webkit-scrollbar-thumb {
  background: #C96868; border-radius: 10px;
}
.perfumes-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #b35252;
}
.perfumes-scroll-container { /* Firefox scrollbar for perfume list */
  scrollbar-width: thin;
  scrollbar-color: #C96868 #f1f1f1;
}

/* Scrollbar for the main .part2-scrollable-content */
.part2-scrollable-content::-webkit-scrollbar {
  width: 10px;
}
.part2-scrollable-content::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.05); border-radius: 10px;
}
.part2-scrollable-content::-webkit-scrollbar-thumb {
  background: #D1D5DB; border-radius: 10px;
}
.part2-scrollable-content::-webkit-scrollbar-thumb:hover {
  background: #9CA3AF;
}
.part2-scrollable-content { /* Firefox main scrollbar */
  scrollbar-width: auto;
  scrollbar-color: #D1D5DB rgba(0,0,0,0.05);
}

.text-xs_NO_FONT_SIZES_HERE {
  font-size: 0.75rem;
  line-height: 1rem;
}
</style>