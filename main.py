from PIL import Image, ImageDraw, ImageFont

def generate_handwritten_text_with_transparency(text, font_path, output_image, line_spacing=5, max_width=2480):
    # Define A4 page size in pixels (2480 x 3508 pixels at 300 DPI)
    a4_width, a4_height = 2480, 3508

    # Load your custom font at a fixed size
    font_size = 150  # Adjust the font size as needed
    font = ImageFont.truetype(font_path, font_size)

    # Split the text into words for wrapping
    words = text.split(' ')
    
    # Variables for dynamic line wrapping
    lines = []
    current_line = ""
    
    # Wrap text to fit within max_width
    for word in words:
        test_line = current_line + word + " "
        text_bbox = ImageDraw.Draw(Image.new('RGBA', (1, 1))).textbbox((0, 0), test_line, font=font)  # Get bounding box for the test line
        test_line_width = text_bbox[2] - text_bbox[0]  # Calculate width from bounding box

        if test_line_width <= max_width:
            current_line = test_line  # Add word to the current line
        else:
            lines.append(current_line.strip())  # Save the current line
            current_line = word + " "  # Start a new line with the current word

    # Append the last line
    if current_line:
        lines.append(current_line.strip())

    # Function to render a page of text
    def render_page(lines_to_render):
        img = Image.new('RGBA', (a4_width, a4_height), color=(255, 255, 255, 0))  # Use RGBA for transparency
        d = ImageDraw.Draw(img)

        # Starting position for the text
        x, y = 50, 50  # Add some margin for readability

        # List to store lines that overflow to the next page
        overflow_lines = []

        for line in lines_to_render:
            text_bbox = d.textbbox((x, y), line, font=font)  # Calculate bounding box for the line
            text_height = text_bbox[3] - text_bbox[1]
            if y + text_height > a4_height:
                overflow_lines.append(line)  # Store the overflowing line
            else:
                d.text((x, y), line, font=font, fill='black')
                y += text_height + line_spacing  # Move to the next line
        
        return img, overflow_lines  # Return the image and remaining lines

    remaining_lines = lines  # All lines initially

    # Generate pages until all lines are rendered
    page_number = 1
    while remaining_lines:
        img, remaining_lines = render_page(remaining_lines)
        img.save(output_image.replace('.png', f'_page_{page_number}.png'))  # Save the current page
        page_number += 1  # Increment the page number

# Example usage
font_path = "my_font.ttf"  # Path to your handwriting font
output_image = "handwritten_output_transparent.png"  # Image file to save

text = """Die Welt wird oft als sinnlos betrachtet aus verschiedenen philosophischen und existenziellen Gründen:

x Fehlende objektive Bedeutung: Es gibt keinen universellen, absoluten Sinn, der für alle Menschen oder das gesamte Universum gilt. Jeder Mensch hat individuelle Perspektiven und Werte, und es gibt keine höhere Macht oder Wahrheit, die diese einen würde.

x Zufälligkeit des Lebens: Viele Ereignisse im Leben und in der Natur erscheinen zufällig und chaotisch. Krankheiten, Unglücke und der Tod geschehen oft ohne Vorwarnung oder erkennbaren Grund, was den Eindruck verstärkt, dass das Leben willkürlich ist.

x Unvollständige Antworten: Menschen suchen nach Antworten auf grundlegende Fragen wie „Warum existieren wir?“ oder „Was ist der Zweck des Lebens?“. Die Unfähigkeit, zufriedenstellende Antworten zu finden, führt zu einem Gefühl der Sinnlosigkeit.

x Die Vergänglichkeit des Lebens: Die Endlichkeit des Lebens und die Unausweichlichkeit des Todes machen viele Menschen bewusst, dass alles, was wir erreichen oder erleben, letztendlich vorübergehend ist. Dies kann zu einem Gefühl der Bedeutungslosigkeit führen.

x Kulturelle und soziale Einflüsse: In modernen Gesellschaften, die oft von Materialismus und Konsum geprägt sind, kann der Fokus auf äußere Erfolge und materielle Besitztümer den inneren Sinn des Lebens in den Hintergrund drängen.

Diese Perspektiven sind zentrale Themen im Absurdismus, der aufzeigt, dass die Absurdität des Lebens nicht als Hindernis, sondern als Anstoß zur Schaffung eigener Bedeutungen und Werte betrachtet werden kann."""


generate_handwritten_text_with_transparency(text, font_path, output_image, line_spacing=5)
