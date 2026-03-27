# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_fake_building_plan(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "RESIDENTIAL REMODEL PLAN")

    # Details
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "Project Address: 123 Main St, San Paloma, CA 95050")
    c.drawString(100, height - 170, "Project Type: Kitchen Remodel & Structural Modification")
    c.drawString(100, height - 190, "Square Footage: 400 sq ft remodel area")

    # Specifications
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 230, "Specifications:")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 250, "1. Structural: Remove load-bearing wall, install 4x12 glu-lam beam.")
    c.drawString(100, height - 270, "2. Electrical: Upgrade main electrical panel to 200 Amps.")
    c.drawString(100, height - 290, "3. Plumbing: Relocate kitchen sink and install new dishwasher supply line.")
    c.drawString(100, height - 310, "4. Lighting: 100% high-efficacy LED recessed lighting.")
    c.drawString(100, height - 330, "5. Insulation: R-15 mineral wool batts in altered exterior walls.")

    # Drawings (Fake)
    c.rect(100, height - 600, 400, 200)
    c.drawString(250, height - 500, "Kitchen Layout & Beam Diagram")

    # Save
    c.save()

if __name__ == "__main__":
    output_path = "sample_kitchen_plan.pdf"
    create_fake_building_plan(output_path)
    print(f"Created fake building plan at: {output_path}")
