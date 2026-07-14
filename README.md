# PDF Shuttle

<div align="center">
  <h1>PDF Shuttle</h1>
  <p>
    <strong>Free, Private & Browser-Based PDF Tools</strong>
  </p>
  <p>
    Merge, split, compress, convert, and edit PDF files online without uploading to servers.
  </p>
</div>

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)
![React](https://img.shields.io/badge/React-19-blue?style=flat-square&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-38bdf8?style=flat-square&logo=tailwindcss)

</div>

**🔗 Try it live: [Free browser-based PDF tools — merge, split, compress & convert](https://pdf.shuttlelab.org)** — 90+ tools that run entirely in your browser, no uploads.

## About

**PDF Shuttle** is a comprehensive suite of PDF tools designed for privacy and performance. Unlike many online converters, PDF Shuttle processes your files entirely within your browser using WebAssembly technology. Your documents **never** leave your device, ensuring maximum security for your sensitive data.

This project is built with modern web technologies to provide a slick, app-like experience directly in the browser.

## Key Features

- **100% Private**: All processing happens client-side. No file uploads to external servers.
- **Fast & Responsive**: Powered by Next.js and WebAssembly for near-native performance.
- **Comprehensive Toolset**: 90+ tools to handle any PDF task.
- **Modern UI**: Clean, accessible, and responsive design built with Tailwind CSS.
- **Multi-language**: Supports 14 languages including English, Chinese, Japanese, Korean, and more.

## Tech Stack

- **Framework**: [Next.js 15](https://nextjs.org/) (App Router)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
- **UI Components**: Custom Tailwind components (shadcn-inspired primitives)
- **PDF Processing**:
  - [PDF.js](https://github.com/mozilla/pdf.js)
  - [pdf-lib](https://github.com/Hopding/pdf-lib)
  - [PyMuPDF (WASM)](https://pymupdf.readthedocs.io/)
- **State Management**: [Zustand](https://github.com/pmndrs/zustand)
- **Deployment**: [Cloudflare Workers](https://workers.cloudflare.com/) via [OpenNext](https://opennext.js.org/)

## Getting Started

### Prerequisites

- Node.js 18.17 or later
- npm, yarn, or pnpm

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShuttleLab/pdf-shuttle.git
   cd pdf-shuttle
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000) to see the application running.

## Deployment

PDF Shuttle is deployed on Cloudflare Workers using OpenNext.

```bash
npm run deploy
```

## Modifications

PDF Shuttle is a modified version of PDFCraft, forked in May 2026 by ShuttleLab.
See [NOTICE.md](./NOTICE.md) for the full list of modifications and required AGPL-3.0 attribution.

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

This project is based on [PDFCraft](https://github.com/PDFCraftTool/pdfcraft), licensed under AGPL-3.0.

---

<div align="center">
  Built by <a href="https://github.com/ShuttleLab">ShuttleLab</a>
</div>
 