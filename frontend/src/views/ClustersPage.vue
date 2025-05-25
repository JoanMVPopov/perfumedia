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
              <select v-model="filters.pcaAnalysis.decade" id="pcaDecade" class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500">
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-full sm:w-32">
              <label for="pcaGender" class="text-sm font-medium">Gender</label>
              <select v-model="filters.pcaAnalysis.gender" id="pcaGender" class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500">
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
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
          <div v-if="images.pcaOverview.length > 0" class="mt-6 flex justify-center items-start">
            <ul class="space-y-8 w-full max-w-4xl">
              <li v-for="(group, groupIndex) in images.pcaOverview" :key="'pca-overview-' + group.filename + '-' + groupIndex" class="border-b pb-6 mb-6">
                <h3 class="text-lg font-semibold mb-3 text-center">{{ group.title }}</h3>
                <div class="relative flex justify-center items-stretch">
                  <div class="flex-shrink-0 max-w-[70%]">
                    <img :src="'data:image/png;base64,' + group.base64" :alt="group.title" class="w-full h-auto rounded-md shadow-md object-contain"/>
                  </div>
                  <div class="relative pl-2 transition-all duration-1000" :class="[expandedIndicesPcaOverview.includes(groupIndex) ? 'w-80' : 'w-24']">
                    <div class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"
                         @click="toggleExplanation(groupIndex, expandedIndicesPcaOverview, displayedTextPcaOverview, textToDisplayPca.overview, images.pcaOverview)">
                      {{ expandedIndicesPcaOverview.includes(groupIndex) ? 'Hide Info' : 'More Info' }}
                    </div>
                    <transition name="fade">
                      <div v-if="expandedIndicesPcaOverview.includes(groupIndex)" class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2 max-h-96 overflow-y-auto">
                        <h4 class="font-bold mb-2">Explanation</h4>
                        <p class="text-sm whitespace-pre-wrap">{{ displayedTextPcaOverview[groupIndex] }}</p>
                      </div>
                    </transition>
                  </div>
                </div>
              </li>
            </ul>
          </div>
          <p v-else-if="attemptedFetchPcaOverview && !loadingPcaOverview" class="mt-6 text-gray-500 text-center">
              No PCA Overview images found for the selected filters.
          </p>
        </div>


        <!-- ========== PART 2: CURATED CLUSTER DETAILS (Violin, Pie, Histograms for specific algo & DR viz) ========== -->
        <div class="mb-6 pb-6 border-b">
            <h2 class="text-xl font-semibold mb-4">2. View Specific Curated Cluster Details</h2>
            <p class="text-xs mb-2 text-gray-500">
              Uses the Decade/Gender from above. Select a clustering algorithm (applied after PCA) and a method to visualize these clusters in 2D.
              This will show the 2D visualization and detailed characteristics (violin, pie, histograms) for each cluster from the selected algorithm.
            </p>
            <div class="flex flex-wrap gap-x-4 gap-y-4 items-end">
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
             <!-- Error Message for Curated Cluster Details -->
            <p v-if="errorCuratedDetails" class="mt-4 text-red-600 font-medium text-center">
                {{ errorCuratedDetails }}
            </p>
            <!-- Display Area for Curated Cluster Detail Images -->
            <div v-if="images.curatedClusterDetails.length > 0" class="mt-6 flex justify-center items-start">
              <ul class="space-y-8 w-full max-w-4xl">
                <li v-for="(group, groupIndex) in images.curatedClusterDetails" :key="'curated-detail-' + group.filename + '-' + groupIndex" class="border-b pb-6 mb-6">
                    <h3 class="text-lg font-semibold mb-3 text-center">{{ group.title }}</h3>
                    <div class="relative flex justify-center items-stretch">
                        <div class="flex-shrink-0 max-w-[70%]">
                            <img :src="'data:image/png;base64,' + group.base64" :alt="group.title" class="w-full h-auto rounded-md shadow-md object-contain"/>
                        </div>
                        <div class="relative pl-2 transition-all duration-1000" :class="[expandedIndicesCuratedDetails.includes(groupIndex) ? 'w-80' : 'w-24']">
                            <!-- ***** THIS BUTTON COLOR IS NOW CORRECTED ***** -->
                            <div class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"
                                @click="toggleExplanation(groupIndex, expandedIndicesCuratedDetails, displayedTextCuratedDetails, textToDisplayPca.details, images.curatedClusterDetails)">
                                {{ expandedIndicesCuratedDetails.includes(groupIndex) ? 'Hide Info' : 'More Info' }}
                            </div>
                            <transition name="fade">
                                <div v-if="expandedIndicesCuratedDetails.includes(groupIndex)" class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2 max-h-96 overflow-y-auto">
                                    <h4 class="font-bold mb-2">Explanation</h4>
                                    <p class="text-sm whitespace-pre-wrap">{{ displayedTextCuratedDetails[groupIndex] }}</p>
                                </div>
                            </transition>
                        </div>
                    </div>
                </li>
              </ul>
            </div>
            <p v-else-if="attemptedFetchCuratedDetails && !loadingCuratedDetails" class="mt-6 text-gray-500 text-center">
                No Curated Cluster Detail images found for the selected algorithm and DR method.
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
        </p>
        <div class="mb-6 flex flex-col items-start">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>
          <div class="flex flex-wrap gap-x-4 gap-y-4 items-end">
            <div class="flex flex-col w-full sm:w-32">
              <label for="otherDrDecade" class="text-sm font-medium">Decade</label>
              <select v-model="filters.otherDrAnalysis.decade" id="otherDrDecade" class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500">
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-full sm:w-32">
              <label for="otherDrGender" class="text-sm font-medium">Gender</label>
              <select v-model="filters.otherDrAnalysis.gender" id="otherDrGender" class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500">
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
            <div class="flex flex-col w-full sm:w-40">
              <label for="otherDrMethod" class="text-sm font-medium">DR Method</label>
              <select v-model="filters.otherDrAnalysis.drMethod" id="otherDrMethod" class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500">
                <option v-for="method in drMethods" :key="method.value" :value="method.value">
                  {{ method.name }}
                </option>
              </select>
            </div>
            <div>
              <button @click="fetchOtherDrAnalysis" :disabled="loadingOtherDr" class="bg-[#C96868] text-white py-2 px-4 rounded-md hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]">
                {{ loadingOtherDr ? "Loading..." : "Get " + selectedDrMethodDisplay + " Analysis" }}
              </button>
            </div>
          </div>
        </div>
        <p v-if="errorOtherDr" class="mt-4 text-red-600 font-medium text-center">{{ errorOtherDr }}</p>
        <div v-if="images.otherDrAnalysis.length > 0" class="mt-6 flex justify-center items-start">
          <ul class="space-y-8 w-full max-w-4xl">
            <li v-for="(group, groupIndex) in images.otherDrAnalysis" :key="'otherdr-group-' + group.filename + '-' + groupIndex" class="border-b pb-6 mb-6">
              <h3 class="text-lg font-semibold mb-3 text-center">{{ group.title }}</h3>
              <div class="relative flex justify-center items-stretch">
                <div class="flex-shrink-0 max-w-[70%]">
                  <img :src="'data:image/png;base64,' + group.base64" :alt="group.title" class="w-full h-auto rounded-md shadow-md object-contain"/>
                </div>
                <div class="relative pl-2 transition-all duration-1000" :class="[expandedIndicesOtherDr.includes(groupIndex) ? 'w-80' : 'w-24']">
                  <div class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm rounded shadow-sm flex items-center justify-center cursor-pointer select-none"
                       @click="toggleExplanation(groupIndex, expandedIndicesOtherDr, displayedTextOtherDr, textToDisplayOtherDr, images.otherDrAnalysis)">
                    {{ expandedIndicesOtherDr.includes(groupIndex) ? 'Hide Info' : 'More Info' }}
                  </div>
                  <transition name="fade">
                    <div v-if="expandedIndicesOtherDr.includes(groupIndex)" class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2 max-h-96 overflow-y-auto">
                      <h4 class="font-bold mb-2">Explanation</h4>
                      <p class="text-sm whitespace-pre-wrap">{{ displayedTextOtherDr[groupIndex] }}</p>
                    </div>
                  </transition>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <p v-else-if="!loadingOtherDr && attemptedFetchOtherDr" class="mt-6 text-gray-500 text-center">
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

export default {
  name: "ClusteringAnalysis",
  components: {
    vSelect,
  },
  data() {
    return {
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
      selectedCuratedClusteringMethod: null,
      selectedCuratedDrMethod: null,

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
        pcaAnalysis: {
          decade: "1990",
          gender: "Masculine",
        },
        otherDrAnalysis: {
          decade: "1990",
          gender: "Masculine",
          drMethod: "umap",
        },
      },
      images: {
        pcaOverview: [], // For PCA variance, loadings, general curated viz
        curatedClusterDetails: [], // For specific cluster characteristics (violin, pie, histo) + specific DR viz
        otherDrAnalysis: [],
      },
      drMethods: [
          { name: "UMAP", value: "umap"},
          { name: "t-SNE", value: "tsne"},
          { name: "LLE", value: "lle"},
          { name: "Isomap", value: "isomap"}
      ],

      textToDisplayPca: { // Explanations for Section I
        overview: { // Texts for images in images.pcaOverview
            DEFAULT: "General explanation for PCA overview plots. These illustrate initial PCA results like variance explained and feature contributions.",
            PCA_VARIANCE: "This plot shows the percentage of dataset variance captured by each principal component (PC) and the cumulative variance. It helps determine how many PCs are needed to represent most of the data's information.",
            PCA_LOADINGS: "PCA loadings indicate how much each original feature contributes to a principal component. Larger absolute values mean a stronger influence of that feature on the PC. This helps interpret what each PC represents.",
            GENERAL_CURATED_VIZ: "This is a general 2D visualization (e.g., UMAP or t-SNE) of the data after initial PCA reduction, showing an overview of clusters found by various algorithms. Specific details per algorithm are below."
        },
        details: { // Texts for images in images.curatedClusterDetails
            DEFAULT: "Detailed explanation for specific curated cluster plots. These show characteristics of individual clusters or their visualization.",
            CURATED_ALGO_VIZ: "This is a 2D visualization (using the selected DR method like UMAP or t-SNE) of the data *after initial PCA reduction*, with points colored by clusters found by the *selected clustering algorithm*. It helps assess cluster separation for this specific algorithm.",
            CLUSTER_RATINGS_VIOLIN: "Violin plots show the distribution of user ratings (e.g., scent, longevity) for perfumes within this specific cluster. The shape indicates data density, and comparison across clusters can reveal distinct preferences.",
            CLUSTER_CATEGORIES_PIE: "Pie charts display the average composition of fragrance categories (e.g., Type, Style, Season, Occasion) for perfumes within this cluster. 'Others' typically groups categories with small percentages. This highlights the dominant fragrance profiles of the cluster.",
            CLUSTER_NOTES_HISTOGRAM: "This histogram shows the frequency of the top fragrance notes for perfumes belonging to this specific cluster, highlighting its dominant scent characteristics and ingredients."
        }
      },
      displayedTextPcaOverview: [],
      expandedIndicesPcaOverview: [],
      displayedTextCuratedDetails: [],
      expandedIndicesCuratedDetails: [],

      textToDisplayOtherDr: { /* Same as before: DR_VIZ, CLUSTER_RATINGS_VIOLIN, etc. */
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
    getExplanationText(imageTitle, textMapForSection) {
        if (!imageTitle || !textMapForSection) return textMapForSection?.DEFAULT || "No explanation available.";
        const titleLower = imageTitle.toLowerCase();

        // Specific to PCA Overview or Curated Details (textMapForSection will be textToDisplayPca.overview or textToDisplayPca.details)
        if (textMapForSection === this.textToDisplayPca.overview) {
            if (titleLower.includes("explained variance")) return textMapForSection.PCA_VARIANCE || textMapForSection.DEFAULT;
            if (titleLower.includes("loadings")) return textMapForSection.PCA_LOADINGS || textMapForSection.DEFAULT;
            if (titleLower.includes("curated") && titleLower.includes("all_clustering_algos")) return textMapForSection.GENERAL_CURATED_VIZ || textMapForSection.DEFAULT; // Example condition for generic overview viz
        }

        if (textMapForSection === this.textToDisplayPca.details) {
             if (titleLower.includes("ratings violin") || titleLower.includes("violin plots")) return textMapForSection.CLUSTER_RATINGS_VIOLIN || textMapForSection.DEFAULT;
            if (titleLower.includes("categories pie") || titleLower.includes("avg categories piecharts")) return textMapForSection.CLUSTER_CATEGORIES_PIE || textMapForSection.DEFAULT;
            if (titleLower.includes("notes histogram")) return textMapForSection.CLUSTER_NOTES_HISTOGRAM || textMapForSection.DEFAULT;
            // Condition for the specific 2D viz of the selected algorithm and DR
            if (titleLower.includes("curated") && (titleLower.includes(this.selectedCuratedDrMethod?.value) || titleLower.includes("2d visualization")) && titleLower.includes(this.selectedCuratedClusteringMethod?.value.toLowerCase())) return textMapForSection.CURATED_ALGO_VIZ || textMapForSection.DEFAULT;
        }

        // For Other DR Section (textMapForSection will be textToDisplayOtherDr)
        if (textMapForSection === this.textToDisplayOtherDr) {
            if (titleLower.includes("ratings violin") || titleLower.includes("violin plots")) return textMapForSection.CLUSTER_RATINGS_VIOLIN || textMapForSection.DEFAULT;
            if (titleLower.includes("categories pie") || titleLower.includes("avg categories piecharts")) return textMapForSection.CLUSTER_CATEGORIES_PIE || textMapForSection.DEFAULT;
            if (titleLower.includes("notes histogram")) return textMapForSection.CLUSTER_NOTES_HISTOGRAM || textMapForSection.DEFAULT;
          if (titleLower.includes("2d visualization") || titleLower.includes("umap") || titleLower.includes("tsne") || titleLower.includes("lle") || titleLower.includes("isomap")) return textMapForSection.DR_VIZ || textMapForSection.DEFAULT;
        }

      return textMapForSection?.DEFAULT || "Explanation details not found for this image.";
    },

    typeText(targetDisplayedTextArray, textToDisplayForThisImage, textIndex) {
      let currentCharacterIndex = 0;
      this.$set(targetDisplayedTextArray, textIndex, "");
      const interval = setInterval(() => {
        if (currentCharacterIndex < textToDisplayForThisImage.length) {
          this.$set(targetDisplayedTextArray, textIndex, targetDisplayedTextArray[textIndex] + textToDisplayForThisImage[currentCharacterIndex]);
          currentCharacterIndex++;
        } else {
          clearInterval(interval);
        }
      }, 15);
    },

    toggleExplanation(index, expandedIndicesArray, targetDisplayedTextArray, sourceTextMapForSection, currentImageList) {
      const i = expandedIndicesArray.indexOf(index);
      const imageTitle = currentImageList[index]?.title || "";
      if (i > -1) {
        expandedIndicesArray.splice(i, 1);
        this.$set(targetDisplayedTextArray, index, "");
      } else {
        // Optional: Collapse others in the same list before expanding a new one
        // while(expandedIndicesArray.length > 0) {
        //   const oldIdx = expandedIndicesArray.pop();
        //   this.$set(targetDisplayedTextArray, oldIdx, "");
        // }
        expandedIndicesArray.push(index);
        const specificExplanation = this.getExplanationText(imageTitle, sourceTextMapForSection);
        this.typeText(targetDisplayedTextArray, specificExplanation, index);
      }
    },

    async fetchPcaAnalysis() { // Fetches PCA Overview (variance, loadings, generic curated viz)
      this.loadingPcaOverview = true;
      this.errorPcaOverview = "";
      this.attemptedFetchPcaOverview = true;
      this.images.pcaOverview = []; // Clear only overview images
      this.expandedIndicesPcaOverview = [];
      this.displayedTextPcaOverview = [];

      try {
        const response = await apiClient.get("/test/clustering-pca-analysis", {
          params: this.filters.pcaAnalysis,
        });
        this.images.pcaOverview = response.data.images || [];
        if (this.images.pcaOverview.length > 0) {
          this.displayedTextPcaOverview = Array(this.images.pcaOverview.length).fill("");
        }
      } catch (err) {
        console.error("Error fetching PCA overview:", err.response?.data?.error || err.message);
        this.errorPcaOverview = err.response?.data?.error || "Failed to fetch PCA overview data.";
        this.images.pcaOverview = [];
      } finally {
        this.loadingPcaOverview = false;
      }
    },

    async fetchCuratedClusterDetails() { // Fetches specific curated cluster characteristics + its DR viz
      if (!this.selectedCuratedClusteringMethod || !this.selectedCuratedDrMethod) {
        this.errorCuratedDetails = "Please select both a clustering algorithm and a visualization DR method.";
        return;
      }
      this.loadingCuratedDetails = true;
      this.errorCuratedDetails = "";
      this.attemptedFetchCuratedDetails = true;
      this.images.curatedClusterDetails = []; // Clear specific details images
      this.expandedIndicesCuratedDetails = [];
      this.displayedTextCuratedDetails = [];

      try {
        const params = {
          decade: this.filters.pcaAnalysis.decade, // Use decade/gender from the common PCA filter section
          gender: this.filters.pcaAnalysis.gender,
          clustering_method: this.selectedCuratedClusteringMethod.value,
          dr_method: this.selectedCuratedDrMethod.value
        };
        const response = await apiClient.get("/test/clustering-curated-cluster-details/", {params});
        this.images.curatedClusterDetails = response.data.images || [];
        if (this.images.curatedClusterDetails.length > 0) {
          this.displayedTextCuratedDetails = Array(this.images.curatedClusterDetails.length).fill("");
        }
      } catch (err) {
        console.error("Error fetching curated cluster details:", err.response?.data?.error || err.message);
        this.errorCuratedDetails = err.response?.data?.error || `Failed to fetch details for ${this.selectedCuratedClusteringMethod.label} with ${this.selectedCuratedDrMethod.label} visualization.`;
        this.images.curatedClusterDetails = [];
      } finally {
        this.loadingCuratedDetails = false;
      }
    },

    async fetchOtherDrAnalysis() {
      this.loadingOtherDr = true;
      this.errorOtherDr = "";
      this.attemptedFetchOtherDr = true;
      this.images.otherDrAnalysis = [];
      this.expandedIndicesOtherDr = [];
      this.displayedTextOtherDr = [];

      try {
        const response = await apiClient.get("/test/clustering-other-dr-analysis", {
          params: this.filters.otherDrAnalysis,
        });
        this.images.otherDrAnalysis = response.data.images || [];
        if (this.images.otherDrAnalysis.length > 0) {
          this.displayedTextOtherDr = Array(this.images.otherDrAnalysis.length).fill("");
        }
      } catch (err) {
        console.error("Error fetching Other DR analysis:", err.response?.data?.error || err.message);
        this.errorOtherDr = err.response?.data?.error || `Failed to fetch ${this.selectedDrMethodDisplay} analysis data.`;
        this.images.otherDrAnalysis = [];
      } finally {
        this.loadingOtherDr = false;
      }
    },
  },
};
</script>

<style scoped>
/* @import 'vue-select/dist/vue-select.css'; */

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

:deep(.vs__dropdown-toggle) {
  border-radius: 0.375rem;
  border: 1px solid #D1D5DB;
  padding: 0.375rem 0.75rem;
  min-height: 2.5rem;
}

:deep(.vs__selected-options) {
  padding: 0;
}

:deep(.vs__selected) {
  margin: 0;
  padding: 0.125rem 0;
  font-size: 0.875rem;
  color: #1F2937;
}

:deep(.vs__search) {
  font-size: 0.875rem;
  padding: 0.125rem 0;
}

:deep(.vs__actions .vs__clear),
:deep(.vs__actions .vs__open-indicator) {
  fill: #6B7280;
  transform: scale(0.8);
}

:deep(.vs__dropdown-menu) {
  border-color: #D1D5DB;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

:deep(.vs__dropdown-option) {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}

:deep(.vs__dropdown-option--highlight) {
  background-color: #E0A9A9;
  color: white;
}
</style>