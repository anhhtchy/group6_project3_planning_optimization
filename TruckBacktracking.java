package class124193.pqd;

import java.io.File;
import java.util.Scanner;

public class TruckBacktracking {
	
	/*
	// this class can be used to check non-ovellap constraint
	class Truck {
		boolean[][] isUsed;
		public Truck(int W, int L) {
			this.isUsed = new boolean[W][L];
			for(int x = 0; x < W; x++) {
				for(int y = 0; y < L; y++) {
					this.isUsed[x][y] = false;
				}
			}
		}
	}
	*/
	
	int N;
	int K;
	int[][] w;
	int[][] l;
	int[] W;
	int[] L;
	int[] c;
	
	int maxW = 0;
	int maxL = 0;
	int sumC = 0;
	
//	Truck[] truck;
	// decision variables
	int[] x1;
	int[] y1;
	int[] p;
	int[] o;
	int[] u;
	
	int[] x1Best;
	int[] y1Best;
	int[] pBest;
	int[] oBest;
	
	int cost = 0;
	int costBest = Integer.MAX_VALUE;
	
	public boolean canPut(int i, int j, int x1i, int y1i, int oi) {
		int x2i = x1i + w[i][oi];
		int y2i = y1i + l[i][oi];
		if(x2i > W[j] || y2i > L[j]) {
//			System.out.printf("%d out of %d", i, j);
			return false;
		}
		for(int i2 = 0; i2 < i; i2++) {
			if(p[i2] == j) {
				int x2i2 = x1[i2] + w[i2][o[i2]];
				int y2i2 = y1[i2] + l[i2][o[i2]];
				if(!((x2i2 <= x1i)
					|| (x2i <= x1[i2])
					|| (y2i2 <= y1i)
					|| (y2i <= y1[i2]))) {
//					System.out.printf("%d overlap with %d\n", i, i2);
					return false;
				}
			}
		}
		return true;
	}
	
	public void put(int i, int j, int x1i, int y1i, int oi) {
		p[i] = j;
		x1[i] = x1i;
		y1[i] = y1i;
		o[i] = oi;
		if(u[j] == 0) {
			cost += c[j];
		}
		u[j] += 1;
	}
	
	public void pop(int j) {
		if(u[j] == 1) {
			cost -= c[j];
		}
		u[j] -= 1;
	}
	
	public void updateBest() {
		costBest = cost;
		for(int i = 0; i < N; i++) {
			x1Best[i] = x1[i];
			y1Best[i] = y1[i];
			pBest[i] = p[i];
			oBest[i] = o[i];
		}
		System.out.println(costBest);
	}
	
	public void TRY(int i) {
		for(int j = 0; j < K; j++) {
			for(int x1i = 0; x1i < W[j]; x1i++) {
				for(int y1i = 0; y1i < L[j]; y1i++) {
					for(int oi = 0; oi <= 1; oi++) {
						if(canPut(i, j, x1i, y1i, oi)) {
							put(i, j, x1i, y1i, oi);
							if(i < N-1) {
								if(cost < costBest) {
									TRY(i+1);
								}
							} else {
//								printResult();
								if(cost < costBest) {
									updateBest();
//									printResult();
								}
							}
							pop(j);
						}
					}
				}
			}
		}
	}
	
	public void init() {
		x1 = new int[N];
		y1 = new int[N];
		p = new int[N];
		o = new int[N];
		u = new int[K];
//		truck = new Truck[K];
		for(int j = 0; j < K; j++) {
			u[j] = 0;
//			truck[j] = new Truck(W[j], L[j]);
		}
		x1Best = new int[N];
		y1Best = new int[N];
		pBest = new int[N];
		oBest = new int[N];
	}
	
	public void readData(String filename) {
		try {
			Scanner in = new Scanner(new File(filename));
			N = in.nextInt();
			K = in.nextInt();
			w = new int[N][2];
			l = new int[N][2];
			int wi = 0;
			int li = 0;
			for(int i = 0; i < N; i++) {
				wi = in.nextInt();
				li = in.nextInt();
				w[i][0] = li;
				w[i][1] = wi;
				l[i][0] = wi;
				l[i][1] = li;
			}
			W = new int[K];
			L = new int[K];
			c = new int[K];
			for(int j = 0; j < K; j++) {
				W[j] = in.nextInt();
				L[j] = in.nextInt();
				c[j] = in.nextInt();
				sumC += c[j];
				if(W[j] > maxW) {
					maxW = W[j];
				}
				if(L[j] > maxL) {
					maxL = L[j];
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public void printData() {
		System.out.println(N + " " + K);
		for(int i = 0; i < N; i++) {
			System.out.println("package "+i+": "+w[i][1]+" "+l[i][1]);
		}
		System.out.println("=========");
		for(int j = 0; j < K; j++) {
			System.out.println("truck "+j+": "+W[j]+" "+L[j]+" "+c[j]);
		}
		System.out.println("=========");
	}
	
	public void printResult() {
		System.out.println("cost = "+costBest);
		for(int i = 0; i < N; i++) {
			int x2i = x1Best[i] + w[i][oBest[i]];
			int y2i = y1Best[i] + l[i][oBest[i]];
			System.out.printf("package %d at truck %d, bottom-left: (%d, %d), upper-right: (%d, %d), orientation: %d\n",
					i, pBest[i], x1Best[i], y1Best[i], x2i, y2i, oBest[i]);
		}
	}
	
	public static void main(String[] args) {
		TruckBacktracking app = new TruckBacktracking();
		app.readData("data/Truck/test-data-1.txt");
		app.printData();
		app.init();
		double t0 = System.currentTimeMillis();
		app.TRY(0);
		double deltaT = System.currentTimeMillis() - t0;
		System.out.println(deltaT);
		app.printResult();
		
		// test result of test-data-1.txt
		/*
		if(app.canPut(0, 5, 5, 0, 1)) {
			app.put(0, 5, 5, 0, 1);
		} else {
			System.out.println("Can't put package 0");
		}
		if(app.canPut(1, 5, 4, 1, 1)) {
			app.put(1, 5, 4, 1, 1);
		} else {
			System.out.println("Can't put package 1");
		}
		if(app.canPut(2, 5, 4, 2, 1)) {
			app.put(2, 5, 4, 2, 1);
		} else {
			System.out.println("Can't put package 2");
		}
		if(app.canPut(3, 5, 0, 4, 0)) {
			app.put(3, 5, 0, 4, 0);
		} else {
			System.out.println("Can't put package 3");
		}
		if(app.canPut(4, 5, 0, 0, 1)) {
			app.put(4, 5, 0, 0, 1);
		} else {
			System.out.println("Can't put package 4");
		}
		if(app.canPut(5, 5, 0, 5, 1)) {
			app.put(5, 5, 0, 5, 1);
		} else {
			System.out.println("Can't put package 5");
		}
		*/
	}

}
