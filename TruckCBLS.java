package class124193.pqd;

import java.io.File;
import java.util.Scanner;

import localsearch.constraints.basic.AND;
import localsearch.constraints.basic.Implicate;
import localsearch.constraints.basic.IsEqual;
import localsearch.constraints.basic.LessOrEqual;
import localsearch.constraints.basic.OR;
import localsearch.functions.basic.FuncMinus;
import localsearch.functions.basic.FuncMult;
import localsearch.functions.basic.FuncPlus;
import localsearch.functions.conditionalsum.ConditionalSum;
import localsearch.model.ConstraintSystem;
import localsearch.model.IConstraint;
import localsearch.model.IFunction;
import localsearch.model.LocalSearchManager;
import localsearch.model.VarIntLS;
import localsearch.search.TabuSearch;

public class TruckCBLS {
	int N;
	int K;
	int[] w;
	int[] l;
	int[] W;
	int[] L;
	int[] c;
	
	int maxW = 0;
	int maxL = 0;
	int sumC = 0;
	//modeling
	LocalSearchManager mgr;
	ConstraintSystem CS;
	VarIntLS[] x1;
	VarIntLS[] y1;
	VarIntLS[] p;
	VarIntLS[] o;
	VarIntLS[] u;
	
	// o=1 <=> x2[i]=x[1]+w[i]
	// o=0 <=> x2[i]=x[1]+l[i]
	// x2[i] = x1[i] + o[i]*w[i] - (o[i]-1)*l[i]
	// y2[i] = y1[i] + o[i]*l[i] - (o[i]-1)*w[i]
	IFunction[] x2;
	IFunction[] y2;
	// of1 = o[i]-1
	// xf1 = o[i]*w[i]
	// xf2 = (o[i]-1)*l[i]
	//because The constructor FuncMinus(int, VarIntLS) is undefined
	// xf3 = o[i]*w[i] - (o[i]-1)*l[i]
	IFunction[] of1;
	IFunction[] xf1;
	IFunction[] xf2;
	IFunction[] xf3;
	IFunction[] yf1;
	IFunction[] yf2;
	IFunction[] yf3;	
	
	IFunction cost;
	public void StateModel() {
		mgr = new LocalSearchManager();
		CS = new ConstraintSystem(mgr);
		x1 = new VarIntLS[N];
		y1 = new VarIntLS[N];
		p = new VarIntLS[N];
		o = new VarIntLS[N];
		u = new VarIntLS[N];
		
		for(int i = 0; i < N; i++) {
			x1[i] = new VarIntLS(mgr, 0, maxW);
			y1[i] = new VarIntLS(mgr, 0, maxL);
			p[i] = new VarIntLS(mgr, 0, K-1);
			o[i] = new VarIntLS(mgr, 0, 1);
			u[i] = new VarIntLS(mgr, 0, 1);
		}
		
		x2 = new IFunction[N];
		y2 = new IFunction[N];
		of1 = new IFunction[N];
		xf1 = new IFunction[N];
		xf2 = new IFunction[N];
		xf3 = new IFunction[N];
		yf1 = new IFunction[N];
		yf2 = new IFunction[N];
		yf3 = new IFunction[N];
		
		for(int i = 0; i < N; i++) {
			of1[i] = new FuncMinus(o[i], 1);
			xf1[i] = new FuncMult(o[i], w[i]);
			xf2[i] = new FuncMult(of1[i], l[i]);
			xf3[i] = new FuncMinus(xf1[i], xf2[i]);
			x2[i] = new FuncPlus(xf3[i], x1[i]);
			
			yf1[i] = new FuncMult(o[i], l[i]);
			yf2[i] = new FuncMult(of1[i], w[i]);
			yf3[i] = new FuncMinus(yf1[i], yf2[i]);
			y2[i] = new FuncPlus(yf3[i], y1[i]);
			
			for(int j = 0; j < K; j++) {
				IConstraint[] cSize = new IConstraint[2];
				cSize[0] = new LessOrEqual(x2[i], W[j]);
				cSize[1] = new LessOrEqual(y2[i], L[j]);
				IsEqual piEqualJ = new IsEqual(p[i], j);
				Implicate implicateSize = new Implicate(piEqualJ, new AND(cSize));
				CS.post(implicateSize);
				// p[i] = j => u[j] = 1
				Implicate implicateUseTruck = new Implicate(piEqualJ, new IsEqual(u[j], 1));
				CS.post(implicateUseTruck);
			}
			
			for(int i2 = i+1; i2 < N; i2++) {
				IConstraint[] cOr = new IConstraint[4];
				cOr[0] = new LessOrEqual(x2[i], x2[i2]);
				cOr[1] = new LessOrEqual(x2[i2], x2[i]);
				cOr[2] = new LessOrEqual(y2[i], y2[i2]);
				cOr[3] = new LessOrEqual(y2[i2], y2[i]);
				Implicate implicate = new Implicate(new IsEqual(p[i], p[i2]), new OR(cOr));
				CS.post(implicate);
			}
		}
		// u[j] = 1 => exist p[i] = j
		for(int j = 0; j < K; j++) {
			IConstraint[] cOr = new IConstraint[N];
			for(int i = 0; i < N; i++) {
				cOr[i] = new IsEqual(p[i], j);
			}
			Implicate implicateUseTruck = new Implicate(new IsEqual(u[j], 1), new OR(cOr));
			CS.post(implicateUseTruck);
		}
		
		cost = new ConditionalSum(u, c, 1);
	}
	public void search() {
		TabuSearch ts = new TabuSearch();
//		ts.greedySearchMinMultiObjectives(cost, CS, 10000, 60000);
	}
	public void readData(String filename) {
		try {
			Scanner in = new Scanner(new File(filename));
			N = in.nextInt();
			K = in.nextInt();
			w = new int[N];
			l = new int[N];
			for(int i = 0; i < N; i++) {
				w[i] = in.nextInt();
				l[i] = in.nextInt();
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
			System.out.println("package "+i+": "+w[i]+" "+l[i]);
		}
		System.out.println("=========");
		for(int j = 0; j < K; j++) {
			System.out.println("truck "+j+": "+W[j]+" "+L[j]+" "+c[j]);
		}
	}
	public static void main(String[] args) {
		TruckCBLS app = new TruckCBLS();
		app.readData("data/Truck/test-data-1.txt");
		app.printData();
	}

}
