import { ImageResponse } from 'next/og';

export const dynamic = 'force-static';
export const revalidate = false;

export async function GET() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#3b82f6',
          borderRadius: '36px',
        }}
      >
        <div
          style={{
            color: 'white',
            fontSize: 64,
            fontWeight: 800,
            letterSpacing: '-2px',
          }}
        >
          PDF
        </div>
      </div>
    ),
    { width: 192, height: 192 }
  );
}
