<template>
  <div class="min-h-screen bg-[#FFF4EA] flex">
    <!-- ========== LEFT STICKY TABLE OF CONTENTS ========== -->
    <aside class="sticky top-20 w-1/6 h-screen border-r p-4 bg-[#FFF4EA] flex-shrink-0">
      <h2 class="text-xl font-bold mb-4">Table of Contents</h2>
      <nav class="flex flex-col space-y-2">
        <!-- Clickable anchor links to each section -->
        <a href="#ratings" class="text-black-500 hover:underline">
          I. RATINGS
        </a>
        <a href="#ratings-progression" class="text-black-500 hover:underline">
          II. RATINGS PROGRESSION
        </a>
        <a href="#categories-and-notes" class="text-black-500 hover:underline">
          III. Categories &amp; Notes
        </a>
        <a href="#correlation" class="text-black-500 hover:underline">
          IV. Correlation
        </a>
        <a href="#brands" class="text-black-500 hover:underline">
          V. Brands
        </a>
      </nav>
    </aside>

    <!-- ========== MAIN CONTENT AREA ========== -->
    <div class="flex-1 p-6">
      <!-- ~~~~~ SECTION I: RATINGS ~~~~~ -->
      <section id="ratings" class="mb-12">
        <h1 class="text-2xl font-bold mb-4">I. RATINGS</h1>

        <!-- ========== FILTERS FOR RATINGS ========== -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold">Select Filters</h2>

          <!-- First row: Set 1 -->
          <div class="flex space-x-4 mt-2">
            <!-- Decade (Set 1) -->
            <div class="flex flex-col w-32">
              <label for="ratingsDecade1" class="text-sm font-medium">Decade</label>
              <select
                v-model="filters.ratings.set1.decade"
                id="ratingsDecade1"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
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
              <label for="ratingsGender1" class="text-sm font-medium">Gender</label>
              <select
                v-model="filters.ratings.set1.gender"
                id="ratingsGender1"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- Plus button toggling second set -->
          <div class="mt-2">
            <button
              @click="toggleSecondOptions('ratings')"
              class="text-indigo-600 text-xl font-bold focus:outline-none hover:text-indigo-800"
            >
              +
            </button>
          </div>

          <!-- Second row: Set 2 (shown if toggled) -->
          <div v-if="showSecondOptions.ratings" class="flex space-x-4 mt-2">
            <!-- Decade (Set 2) -->
            <div class="flex flex-col w-32">
              <label for="ratingsDecade2" class="text-sm font-medium">Decade</label>
              <select
                v-model="filters.ratings.set2.decade"
                id="ratingsDecade2"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
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
              <label for="ratingsGender2" class="text-sm font-medium">Gender</label>
              <select
                v-model="filters.ratings.set2.gender"
                id="ratingsGender2"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- "Get Images" button -->
          <button
            @click="fetchRatings"
            class="mt-4 bg-indigo-600 text-white py-2 px-4 rounded-md
                   hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            Get RATINGS
          </button>
        </div>

        <!-- ========== DISPLAY RATINGS IMAGES ========== -->
        <!-- We check if we have 2 sets => show 2 columns, else show 1 column with typed explanation. -->
        <div
          :class="showTwoColumns('ratings')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- ====== SET 1 IMAGES ====== -->
          <div
            v-if="images.ratings[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">RATINGS - Set 1</h2>

            <!-- If two columns => just images. If single col => typed explanation logic. -->
            <div
              v-if="!showTwoColumns('ratings')"
              class="flex-1 h-full"
            >
              <ul class="space-y-6 px-2">
                <li
                  v-for="(image, index) in images.ratings[0]"
                  :key="'rat1-' + index"
                  class="relative flex justify-center items-stretch border-b pb-4 mb-4"
                >
                  <!-- The image -->
                  <div class="flex-shrink-0 max-w-[50%]">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>

                  <!-- Toggle Explanation w/ typewriter text -->
                  <div
                    class="relative pl-2 transition-all duration-1000"
                    :class="[expandedIndices.includes(index) ? 'w-80' : 'w-24']"
                  >
                    <div
                      class="sticky top-20 z-10 w-24 h-10 bg-blue-100 text-blue-700 font-bold text-sm
                             rounded shadow-sm flex items-center justify-center
                             cursor-pointer select-none"
                      @click="toggleExplanation(index)"
                    >
                      {{ expandedIndices.includes(index) ? 'Hide Info' : 'More Info' }}
                    </div>

                    <transition name="fade">
                      <div
                        v-if="expandedIndices.includes(index)"
                        class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2"
                      >
                        <h3 class="font-bold mb-2">Explanation</h3>
                        <p class="text-sm">
                          <!-- Typed text displayed here -->
                          {{ displayedText[index % textToDisplay.length] }}
                        </p>
                      </div>
                    </transition>
                  </div>
                </li>
              </ul>
            </div>

            <!-- If two columns => just images in a scroll container -->
            <div
              v-else
              class="overflow-y-auto h-full"
            >
              <ul>
                <li
                  v-for="(image, index) in images.ratings[0]"
                  :key="'rat1-col2-' + index"
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

          <!-- ====== SET 2 IMAGES (only if plus sign toggled and data loaded) ====== -->
          <div
            v-if="showSecondOptions.ratings && images.ratings[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">RATINGS - Set 2</h2>
            <div class="overflow-y-auto h-full">
              <ul>
                <li
                  v-for="(image, index) in images.ratings[1]"
                  :key="'rat2-' + index"
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
      </section>

      <!-- ~~~~~ SECTION II: RATINGS PROGRESSION ~~~~~ -->
      <section id="ratings-progression" class="mb-12">
        <h1 class="text-2xl font-bold mb-4">II. RATINGS PROGRESSION</h1>

        <!-- ========== FILTERS (Progression) ========== -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold">Select Filters</h2>

          <!-- First row: Set 1 -->
          <div class="flex space-x-4 mt-2">
            <!-- Decade (all only) -->
            <div class="flex flex-col w-32">
              <label for="progressionDecade1" class="text-sm font-medium">Decade</label>
              <select
                v-model="filters.ratingsProgression.set1.decade"
                id="progressionDecade1"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
              </select>
            </div>
            <!-- Gender (Set 1) -->
            <div class="flex flex-col w-32">
              <label for="progressionGender1" class="text-sm font-medium">Gender</label>
              <select
                v-model="filters.ratingsProgression.set1.gender"
                id="progressionGender1"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- Plus button toggling second set -->
          <div class="mt-2">
            <button
              @click="toggleSecondOptions('ratingsProgression')"
              class="text-indigo-600 text-xl font-bold focus:outline-none hover:text-indigo-800"
            >
              +
            </button>
          </div>

          <!-- Second row: Set 2 (shown if toggled) -->
          <div v-if="showSecondOptions.ratingsProgression" class="flex space-x-4 mt-2">
            <div class="flex flex-col w-32">
              <label for="progressionDecade2" class="text-sm font-medium">Decade</label>
              <select
                v-model="filters.ratingsProgression.set2.decade"
                id="progressionDecade2"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
              </select>
            </div>
            <div class="flex flex-col w-32">
              <label for="progressionGender2" class="text-sm font-medium">Gender</label>
              <select
                v-model="filters.ratingsProgression.set2.gender"
                id="progressionGender2"
                class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <button
            @click="fetchRatingsProgression"
            class="mt-4 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none"
          >
            Get RATINGS PROGRESSION
          </button>
        </div>

        <!-- DISPLAY RATINGS PROGRESSION IMAGES -->
        <div
          :class="showTwoColumns('ratingsProgression')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
            v-if="images.ratingsProgression[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              RATINGS PROGRESSION - Set 1
            </h2>
            <!-- Just a simple display, no typed explanation here (but you could replicate if desired) -->
            <ul>
              <li
                v-for="(image, idx) in images.ratingsProgression[0]"
                :key="'prog1-' + idx"
                class="border-b pb-4 mb-4"
              >
                <img
                  :src="'data:image/png;base64,' + image.base64"
                  alt="Progression Image"
                  class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>

          <!-- Set 2 -->
          <div
            v-if="showSecondOptions.ratingsProgression && images.ratingsProgression[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              RATINGS PROGRESSION - Set 2
            </h2>
            <ul>
              <li
                v-for="(image, idx) in images.ratingsProgression[1]"
                :key="'prog2-' + idx"
                class="border-b pb-4 mb-4"
              >
                <img
                  :src="'data:image/png;base64,' + image.base64"
                  alt="Progression Image"
                  class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ~~~~~ SECTION III: Categories & Notes ~~~~~ -->
      <section id="categories-and-notes" class="mb-12">
        <h1 class="text-2xl font-bold mb-4">III. Categories &amp; Notes</h1>

        <!-- FILTERS -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold">Select Filters</h2>

          <!-- First set -->
          <div class="flex space-x-4 mt-2">
            <!-- Decade (Set 1) -->
            <div class="flex flex-col w-32">
              <label for="catDecade1" class="text-sm font-medium">Decade</label>
              <select
                  v-model="filters.categoriesAndNotes.set1.decade"
                  id="catDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
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
              <label for="catGender1" class="text-sm font-medium">Gender</label>
              <select
                  v-model="filters.categoriesAndNotes.set1.gender"
                  id="catGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- Plus button -->
          <div class="mt-2">
            <button
                @click="toggleSecondOptions('categoriesAndNotes')"
                class="text-indigo-600 text-xl font-bold focus:outline-none hover:text-indigo-800"
            >
              +
            </button>
          </div>

          <!-- Second set -->
          <div v-if="showSecondOptions.categoriesAndNotes" class="flex space-x-4 mt-2">
            <div class="flex flex-col w-32">
              <label for="catDecade2" class="text-sm font-medium">Decade</label>
              <select
                  v-model="filters.categoriesAndNotes.set2.decade"
                  id="catDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-32">
              <label for="catGender2" class="text-sm font-medium">Gender</label>
              <select
                  v-model="filters.categoriesAndNotes.set2.gender"
                  id="catGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- Button -->
          <button
              @click="fetchCategoriesAndNotes"
              class="mt-4 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none"
          >
            Get Categories &amp; Notes
          </button>
        </div>

        <!-- DISPLAY IMAGES -->
        <div
            :class="showTwoColumns('categoriesAndNotes')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
              v-if="images.categoriesAndNotes[0]?.length"
              class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              Categories &amp; Notes - Set 1
            </h2>
            <ul>
              <li
                  v-for="(image, idx) in images.categoriesAndNotes[0]"
                  :key="'cat1-' + idx"
                  class="border-b pb-4 mb-4"
              >
                <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Categories Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>

          <!-- Set 2 -->
          <div
              v-if="showSecondOptions.categoriesAndNotes && images.categoriesAndNotes[1]?.length"
              class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              Categories &amp; Notes - Set 2
            </h2>
            <ul>
              <li
                  v-for="(image, idx) in images.categoriesAndNotes[1]"
                  :key="'cat2-' + idx"
                  class="border-b pb-4 mb-4"
              >
                <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Categories Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ~~~~~ SECTION IV: Correlation ~~~~~ -->
      <section id="correlation" class="mb-12">
        <h1 class="text-2xl font-bold mb-4">IV. Correlation</h1>

        <!-- FILTERS -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold">Select Filters</h2>

          <!-- First set -->
          <div class="flex space-x-4 mt-2">
            <div class="flex flex-col w-32">
              <label for="corrDecade1" class="text-sm font-medium">Decade</label>
              <select
                  v-model="filters.correlation.set1.decade"
                  id="corrDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-32">
              <label for="corrGender1" class="text-sm font-medium">Gender</label>
              <select
                  v-model="filters.correlation.set1.gender"
                  id="corrGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- Plus button -->
          <div class="mt-2">
            <button
                @click="toggleSecondOptions('correlation')"
                class="text-indigo-600 text-xl font-bold focus:outline-none hover:text-indigo-800"
            >
              +
            </button>
          </div>

          <!-- Second set -->
          <div v-if="showSecondOptions.correlation" class="flex space-x-4 mt-2">
            <div class="flex flex-col w-32">
              <label for="corrDecade2" class="text-sm font-medium">Decade</label>
              <select
                  v-model="filters.correlation.set2.decade"
                  id="corrDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-32">
              <label for="corrGender2" class="text-sm font-medium">Gender</label>
              <select
                  v-model="filters.correlation.set2.gender"
                  id="corrGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <button
              @click="fetchCorrelation"
              class="mt-4 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none"
          >
            Get Correlation
          </button>
        </div>

        <!-- DISPLAY IMAGES -->
        <div
            :class="showTwoColumns('correlation')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
              v-if="images.correlation[0]?.length"
              class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              Correlation - Set 1
            </h2>
            <ul>
              <li
                  v-for="(image, idx) in images.correlation[0]"
                  :key="'corr1-' + idx"
                  class="border-b pb-4 mb-4"
              >
                <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Correlation Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>

          <!-- Set 2 -->
          <div
              v-if="showSecondOptions.correlation && images.correlation[1]?.length"
              class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              Correlation - Set 2
            </h2>
            <ul>
              <li
                  v-for="(image, idx) in images.correlation[1]"
                  :key="'corr2-' + idx"
                  class="border-b pb-4 mb-4"
              >
                <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Correlation Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ~~~~~ SECTION V: Brands ~~~~~ -->
      <section id="brands" class="mb-12">
        <h1 class="text-2xl font-bold mb-4">V. Brands</h1>

        <!-- FILTERS -->
        <div class="mb-6">
          <h2 class="text-xl font-semibold">Select Filters</h2>

          <!-- First set -->
          <div class="flex space-x-4 mt-2">
            <div class="flex flex-col w-32">
              <label for="brandsDecade1" class="text-sm font-medium">Decade</label>
              <select
                  v-model="filters.brands.set1.decade"
                  id="brandsDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-32">
              <label for="brandsGender1" class="text-sm font-medium">Gender</label>
              <select
                  v-model="filters.brands.set1.gender"
                  id="brandsGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <!-- Plus button -->
          <div class="mt-2">
            <button
                @click="toggleSecondOptions('brands')"
                class="text-indigo-600 text-xl font-bold focus:outline-none hover:text-indigo-800"
            >
              +
            </button>
          </div>

          <!-- Second set -->
          <div v-if="showSecondOptions.brands" class="flex space-x-4 mt-2">
            <div class="flex flex-col w-32">
              <label for="brandsDecade2" class="text-sm font-medium">Decade</label>
              <select
                  v-model="filters.brands.set2.decade"
                  id="brandsDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="1990">1990s</option>
                <option value="2000">2000s</option>
                <option value="2010">2010s</option>
                <option value="2020">2020s</option>
              </select>
            </div>
            <div class="flex flex-col w-32">
              <label for="brandsGender2" class="text-sm font-medium">Gender</label>
              <select
                  v-model="filters.brands.set2.gender"
                  id="brandsGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
              >
                <option value="All">All</option>
                <option value="Masculine">Masculine</option>
                <option value="Feminine">Feminine</option>
              </select>
            </div>
          </div>

          <button
              @click="fetchBrands"
              class="mt-4 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none"
          >
            Get Brands
          </button>
        </div>

        <!-- DISPLAY IMAGES -->
        <div
            :class="showTwoColumns('brands')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
              v-if="images.brands[0]?.length"
              class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              Brands - Set 1
            </h2>
            <ul>
              <li
                  v-for="(image, idx) in images.brands[0]"
                  :key="'brands1-' + idx"
                  class="border-b pb-4 mb-4"
              >
                <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Brands Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>

          <!-- Set 2 -->
          <div
              v-if="showSecondOptions.brands && images.brands[1]?.length"
              class="flex flex-col w-full mb-4"
          >
            <h2 class="text-lg font-bold mb-2 text-center">
              Brands - Set 2
            </h2>
            <ul>
              <li
                  v-for="(image, idx) in images.brands[1]"
                  :key="'brands2-' + idx"
                  class="border-b pb-4 mb-4"
              >
                <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Brands Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                />
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Error Message -->
      <p v-if="error" class="mt-4 text-red-600 font-medium text-center">
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api"; // or your Axios instance / fetch utility

export default {
  name: "FiveSectionFiltersPlusTypewriter",
  data() {
    return {
      error: "",
      // For toggling second set of filters in each section
      showSecondOptions: {
        ratings: false,
        ratingsProgression: false,
        categoriesAndNotes: false,
        correlation: false,
        brands: false,
      },
      // The user’s typed text placeholders
      textToDisplay: [
        "This is the first placeholder text",
        "This is the second placeholder text",
        "This is the third one",
      ],
      // Where typed text is displayed
      displayedText: ["", "", ""],
      // Indices for which images are expanded (for single-col scenario)
      expandedIndices: [],

      // Each section has 2 sets of filters (like your original code).
      // set1 is always present, set2 is shown if plus sign is toggled.
      filters: {
        ratings: {
          set1: {decade: "All", gender: "All"},
          set2: {decade: "All", gender: "All"},
        },
        ratingsProgression: {
          set1: {decade: "All", gender: "All"},
          set2: {decade: "All", gender: "All"},
        },
        categoriesAndNotes: {
          set1: {decade: "All", gender: "All"},
          set2: {decade: "All", gender: "All"},
        },
        correlation: {
          set1: {decade: "All", gender: "All"},
          set2: {decade: "All", gender: "All"},
        },
        brands: {
          set1: {decade: "All", gender: "All"},
          set2: {decade: "All", gender: "All"},
        },
      },

      // Each section now stores up to 2 arrays of images: images[section][0], images[section][1].
      images: {
        ratings: [[], []],
        ratingsProgression: [[], []],
        categoriesAndNotes: [[], []],
        correlation: [[], []],
        brands: [[], []],
      },
    };
  },
  methods: {
    // === TYPEWRITER METHOD ===
    typeText(textPremade, textIndex) {
      let index = 0;

      // Reset displayed text if previously typed
      if (this.displayedText[textIndex] !== "") {
        this.displayedText[textIndex] = "";
      }

      const interval = setInterval(() => {
        if (index < textPremade.length) {
          this.displayedText[textIndex] += textPremade[index];
          index++;
        } else {
          clearInterval(interval); // Stop when text is fully typed
        }
      }, 20);
    },

    // === TOGGLE EXPLANATION (SINGLE-COL ONLY) ===
    toggleExplanation(index) {
      const i = this.expandedIndices.indexOf(index);
      if (i > -1) {
        // Already expanded => collapse
        this.expandedIndices.splice(i, 1);
        // Clear typed text
        this.displayedText[index % this.textToDisplay.length] = "";
      } else {
        // Expand
        this.expandedIndices.push(index);
        // Trigger typewriter for that index
        this.typeText(
            this.textToDisplay[index % this.textToDisplay.length],
            index % this.textToDisplay.length
        );
      }
    },

    // === TOGGLE SECOND SET OF FILTERS (PLUS SIGN) ===
    toggleSecondOptions(section) {
      this.showSecondOptions[section] = !this.showSecondOptions[section];
    },

    // === CHECK IF WE SHOW 2 COLUMNS OF IMAGES ===
    // e.g., if second set is toggled AND actually has images
    showTwoColumns(section) {
      return (
          this.showSecondOptions[section] &&
          this.images[section][1] &&
          this.images[section][1].length > 0
      );
    },

    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // All the "fetch" methods: each makes 1 or 2 API calls
    // depending on whether second set is toggled
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    async fetchRatings() {
      this.error = "";
      try {
        // Build an array of sets to fetch
        const relevantSets = this.showSecondOptions.ratings
            ? [this.filters.ratings.set1, this.filters.ratings.set2]
            : [this.filters.ratings.set1];

        // Make parallel calls
        const responses = await Promise.all(
            relevantSets.map((opts) =>
                apiClient.get("/test/eda-data", {
                  params: {
                    decade: opts.decade,
                    gender: opts.gender,
                  },
                })
            )
        );

        // Store into images.ratings[0] and [1]
        this.images.ratings[0] = responses[0].data.images || [];
        this.images.ratings[1] = responses[1]?.data?.images || [];
        this.expandedIndices = []; // reset expansions
      } catch (err) {
        console.error(err);
        this.error = "Error fetching RATINGS data.";
      }
    },

    async fetchRatingsProgression() {
      this.error = "";
      try {
        const relevantSets = this.showSecondOptions.ratingsProgression
            ? [
              this.filters.ratingsProgression.set1,
              this.filters.ratingsProgression.set2,
            ]
            : [this.filters.ratingsProgression.set1];

        const responses = await Promise.all(
            relevantSets.map((opts) =>
                apiClient.get("/test/eda-data", {
                  params: {
                    decade: opts.decade,
                    gender: opts.gender,
                  },
                })
            )
        );

        this.images.ratingsProgression[0] = responses[0].data.images || [];
        this.images.ratingsProgression[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error(err);
        this.error = "Error fetching RATINGS PROGRESSION data.";
      }
    },

    async fetchCategoriesAndNotes() {
      this.error = "";
      try {
        const relevantSets = this.showSecondOptions.categoriesAndNotes
            ? [
              this.filters.categoriesAndNotes.set1,
              this.filters.categoriesAndNotes.set2,
            ]
            : [this.filters.categoriesAndNotes.set1];

        const responses = await Promise.all(
            relevantSets.map((opts) =>
                apiClient.get("/test/eda-data", {
                  params: {
                    decade: opts.decade,
                    gender: opts.gender,
                  },
                })
            )
        );

        this.images.categoriesAndNotes[0] = responses[0].data.images || [];
        this.images.categoriesAndNotes[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error(err);
        this.error = "Error fetching Categories & Notes data.";
      }
    },

    async fetchCorrelation() {
      this.error = "";
      try {
        const relevantSets = this.showSecondOptions.correlation
            ? [this.filters.correlation.set1, this.filters.correlation.set2]
            : [this.filters.correlation.set1];

        const responses = await Promise.all(
            relevantSets.map((opts) =>
                apiClient.get("/test/eda-data", {
                  params: {
                    decade: opts.decade,
                    gender: opts.gender,
                  },
                })
            )
        );

        this.images.correlation[0] = responses[0].data.images || [];
        this.images.correlation[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error(err);
        this.error = "Error fetching Correlation data.";
      }
    },

    async fetchBrands() {
      this.error = "";
      try {
        const relevantSets = this.showSecondOptions.brands
            ? [this.filters.brands.set1, this.filters.brands.set2]
            : [this.filters.brands.set1];

        const responses = await Promise.all(
            relevantSets.map((opts) =>
                apiClient.get("/test/eda-data", {
                  params: {
                    decade: opts.decade,
                    gender: opts.gender,
                  },
                })
            )
        );

        this.images.brands[0] = responses[0].data.images || [];
        this.images.brands[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error(err);
        this.error = "Error fetching Brands data.";
      }
    },
  },
};
</script>

<style scoped>
/* Fade transition for typed explanation box (if desired) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Example sticky sidebar ensuring full height */
aside {
  min-height: 100vh;
}
</style>
