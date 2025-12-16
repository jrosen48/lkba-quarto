#!/bin/bash

chapters=(
  "zzz-dedication.qmd"
  "ZZZ - Acknowledgments.qmd"
  "index.qmd"
  "a-story-about-a-hike.qmd"
  "AAA - Considerations_for_Your_First_Hike.qmd"
  "AAA - Finding_a_Hike.qmd"
  "AAA - what each includes.qmd"
  "AAA - overview-of-the-hikes.qmd"
  "AAA - top-5.qmd"
  "Sec - Knoxville.qmd"
  "Trail_1__Seven_Islands.qmd"
  "Trail_2__Ijams_Riverside.qmd"
  "Trail_3__Lakeshore_Park.qmd"
  "Trail_4__High_Ground_Park.qmd"
  "Trail_5__UT_Arboretum.qmd"
  "Trail_6__Knox-Blount_Greenway.qmd"
  "Trail_7__Sequoyah_Park.qmd"
  "Trail_8__Ijams_Crag.qmd"
  "Trail_9__William_Hastie.qmd"
  "Trail_10__Sharp_s_Ridge.qmd"
  "Trail_11__Norris_Dam.qmd"
  "Trail_12__House_Mountain.qmd"
  "Trail_13__Aspire_Park.qmd"
  "Sec - The_Cumberland_Plateau.qmd"
  "Trail_14__Emory_Falls.qmd"
  "Trail_15__Obed_Point.qmd"
  "Trail_16__Bandy_Creek.qmd"
  "Trail_17__Fall_Branch_Falls.qmd"
  "Trail_18__Twin_Arches.qmd"
  "Trail_19__Angel_Falls.qmd"
  "Trail_20___Honey_Creek.qmd"
  "Sec - The_Great_Smoky_Mountains_National_Park.qmd"
  "Trail_21__Spruce_Flats_Falls.qmd"
  "Trail_22__Little_River.qmd"
  "Trail_23__Mouse_Creek.qmd"
  "Trail_24__Middle_Prong.qmd"
  "Trail_25__Abrams_Creek.qmd"
  "Trail_26__Look_Rock.qmd"
  "Trail_27__Chestnut_Top.qmd"
  "Trail_28__Abrams_Falls.qmd"
  "Trail_29__Andrews_Bald.qmd"
  "Trail_30__Alum_Cave_Bluffs.qmd"
  "ZZZ - Deepening_the_Experience.qmd"
  "ZZZ - Recommended_Books__Resources__and_Organizations.qmd"
  "zzz - join and give back.qmd"
  "ZZZ - About_the_Authors.qmd"
  "ZZZ - Appendices.qmd"
)

rm -rf docx_chapters
mkdir -p docx_chapters

# Temporarily rename _quarto.yml to render files as standalone documents
mv _quarto.yml _quarto.yml.bak

i=1
for f in "${chapters[@]}"; do
  echo "Rendering $i: $f"
  output_name="$(printf '%02d' $i)_$(basename "$f" .qmd).docx"
  quarto render "$f" --to docx --output "$output_name"
  mv "$output_name" docx_chapters/
  ((i++))
done

# Restore _quarto.yml
mv _quarto.yml.bak _quarto.yml