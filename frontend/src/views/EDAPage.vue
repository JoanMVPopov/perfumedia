<template>
  <!-- Full-page container so the layout can stretch -->
  <div class="min-h-screen bg-[#fcece4] flex flex-col">
    <!-- (1) Filter Section -->
    <div class="container mx-auto p-6">
      <h1 class="text-2xl font-bold text-center mb-4">Select Filters</h1>

      <!-- Row: Set 1 + Plus + Set 2 -->
      <div class="flex justify-center items-start space-x-8">
        <!-- First set of options -->
        <div class="flex space-x-4">
          <!-- Decade (Set 1) -->
          <div class="flex flex-col w-32">
            <label for="decade1" class="block text-sm font-medium text-gray-700">Decade</label>
            <select
              v-model="selectedOptions[0].decade"
              id="decade1"
              class="mt-1 block rounded-md border-gray-300 shadow-sm
                     focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="All">All</option>
              <option value="1990">1990s</option>
              <option value="2000">2000s</option>
              <option value="2010">2010s</option>
              <option value="2020">2020s</option>
            </select>
          </div>

          <!-- Gender (Set 1) -->
          <div class="flex flex-col w-32">
            <label for="gender1" class="block text-sm font-medium text-gray-700">Gender</label>
            <select
              v-model="selectedOptions[0].gender"
              id="gender1"
              class="mt-1 block rounded-md border-gray-300 shadow-sm
                     focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="All">All</option>
              <option value="Masculine">Masculine</option>
              <option value="Feminine">Feminine</option>
            </select>
          </div>
        </div>

        <!-- Plus button -->
        <div class="self-center">
          <button
            @click="toggleSecondOptions"
            class="text-indigo-600 text-xl font-bold focus:outline-none hover:text-indigo-800"
          >
            +
          </button>
        </div>

        <!-- Second set of options (hidden by default) -->
        <div v-if="showSecondOptions" class="flex space-x-4">
          <!-- Decade (Set 2) -->
          <div class="flex flex-col w-32">
            <label for="decade2" class="block text-sm font-medium text-gray-700">Decade</label>
            <select
              v-model="selectedOptions[1].decade"
              id="decade2"
              class="mt-1 block rounded-md border-gray-300 shadow-sm
                     focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="All">All</option>
              <option value="1990">1990s</option>
              <option value="2000">2000s</option>
              <option value="2010">2010s</option>
              <option value="2020">2020s</option>
            </select>
          </div>

          <!-- Gender (Set 2) -->
          <div class="flex flex-col w-32">
            <label for="gender2" class="block text-sm font-medium text-gray-700">Gender</label>
            <select
              v-model="selectedOptions[1].gender"
              id="gender2"
              class="mt-1 block rounded-md border-gray-300 shadow-sm
                     focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            >
              <option value="All">All</option>
              <option value="Masculine">Masculine</option>
              <option value="Feminine">Feminine</option>
            </select>
          </div>
        </div>
      </div>

      <!-- "Get Images" button -->
      <div class="flex justify-center mt-6">
        <button
          @click="fetchImages"
          class="bg-indigo-600 text-white py-2 px-4 rounded-md
                 hover:bg-indigo-700 focus:outline-none
                 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Get Images
        </button>
      </div>
    </div>

    <!-- (2) Horizontal line divider -->
    <hr class="border-gray-300 mt-2" />

    <!-- (3) Image area -->
    <div class="flex-1 container mx-auto p-6">
      <!--
        If 2 sets are shown, switch to a 2-column grid
        If only 1 set, center it
      -->
      <div
        :class="[
          showTwoColumns
            ? 'grid grid-cols-2 gap-6 h-full'
            : 'flex justify-center items-start h-full'
        ]"
      >
        <!-- Images Set 1 -->
        <div
          v-if="images[0]?.length"
          class="flex flex-col w-full h-full flex-1 mb-4"
        >
          <h2 class="text-xl text-center font-bold mb-4">Images Set 1</h2>

          <!-- SINGLE SCROLL CONTAINER for sticky explanation if only 1 set -->
          <!-- If 2 sets -> no explanation (just show images) -->
          <div
            v-if="!showTwoColumns"
            class="flex-1 h-full"
          >
            <ul class="space-y-6 px-2">
              <li
                v-for="(image, index) in images[0]"
                :key="index"
                class="relative flex border-b pb-4 mb-4"
              >
                <!-- The image (fills column width) -->
                <div class="flex-shrink-0 pr-4">
                  <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Decoded Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                  />
                </div>

                <!-- "More Info" box & Sticky Explanation -->
                <div class="relative flex-grow">
                  <div
                    class="w-24 h-10 bg-blue-100 text-blue-700 font-bold text-sm
                           rounded shadow-sm flex items-center justify-center
                           cursor-pointer select-none"
                    @click="toggleExplanation(index)"
                  >
                    {{ expandedIndices.includes(index) ? 'Hide Info' : 'More Info' }}
                  </div>

                  <transition name="fade">
                    <div
                      v-if="expandedIndices.includes(index)"
                      class="sticky top-20 z-10 bg-white p-4 shadow-md rounded mt-2"
                    >
                      <h3 class="font-bold mb-2">Explanation</h3>
                      <p class="text-sm">
                        This is a detailed explanation for {{ image.filename }}.<br />
                        Multiple items can be open at once!
                      </p>
                    </div>
                  </transition>
                </div>
              </li>
            </ul>
          </div>

          <!-- If 2 columns -> no explanation, just images in a scroll container -->
          <div
            v-else
            class="overflow-y-auto flex-1 h-full"
          >
            <ul class="space-y-6 px-2">
              <li
                v-for="(image, index) in images[0]"
                :key="index"
                class="border-b pb-4 mb-4"
              >
                <img
                  :src="'data:image/png;base64,' + image.base64"
                  alt="Decoded Image"
                  class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>
        </div>

        <!-- Images Set 2 (only shown if 2 sets exist) -->
        <div
          v-if="showTwoColumns && images[1]?.length"
          class="flex flex-col w-full h-full flex-1 mb-4"
        >
          <h2 class="text-xl text-center font-bold mb-4">Images Set 2</h2>
          <div class="overflow-y-auto flex-1 h-full">
            <ul class="space-y-6 px-2">
              <li
                v-for="(image, index) in images[1]"
                :key="index"
                class="border-b pb-4 mb-4"
              >
                <img
                  :src="'data:image/png;base64,' + image.base64"
                  alt="Decoded Image"
                  class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <p v-if="error" class="mt-4 text-red-600 font-medium text-center">
      {{ error }}
    </p>
  </div>
</template>

<script>
import apiClient from "@/api";

export default {
  data() {
    return {
      showSecondOptions: false,
      selectedOptions: [
        { decade: "All", gender: "All" },
        { decade: "All", gender: "All" },
      ],
      images: [[], []],
      error: "",
      expandedIndices: [] // multiple open explanations in single-col mode
    };
  },
  computed: {
    showTwoColumns() {
      return this.showSecondOptions && this.images[1]?.length > 0;
    },
  },
  methods: {
    toggleSecondOptions() {
      this.showSecondOptions = !this.showSecondOptions;
    },
    async fetchImages() {
      try {
        const relevantOptions = this.showSecondOptions
          ? this.selectedOptions
          : [this.selectedOptions[0]];

        const responses = await Promise.all(
          relevantOptions.map((opts) =>
            apiClient.get("/test/eda-data/", {
              params: {
                decade: opts.decade,
                gender: opts.gender,
              },
            })
          )
        );

        // Single set => just store the 0th
        // Two sets => store both
        if (!this.showSecondOptions) {
          this.images[0] = responses[0]?.data?.images || [];
          this.images[1] = [];
        } else {
          this.images = responses.map((res) => res.data.images || []);
        }

        // Reset expansions if new images are loaded
        this.expandedIndices = [];
        this.error = "";
      } catch (err) {
        console.error(err);
        this.error =
          err.response?.data?.error || "An error occurred while fetching images.";
      }
    },
    toggleExplanation(index) {
      // Toggle specific index in expandedIndices
      const i = this.expandedIndices.indexOf(index);
      if (i > -1) {
        this.expandedIndices.splice(i, 1);
      } else {
        this.expandedIndices.push(index);
      }
    },
  },
};
</script>

<style scoped>
/* Fade transition for the collapsible explanation box */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
