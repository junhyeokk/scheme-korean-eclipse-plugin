package schemetest.views;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Group;
import org.eclipse.swt.widgets.Text;

public class form {
	static private Process ps;
	static private BufferedReader br;
//	static private BufferedWriter bw;
	private Group executeGroup;
	final Text t1;
	private Button exe;

	public form(Composite shell) {
		ps = null;
		executeGroup = new Group(shell, SWT.NULL);
		executeGroup.setText("한글 스킴");
		executeGroup.setBounds(25, 25, 800, 700);
		t1 = new Text(executeGroup, SWT.MULTI);
		t1.setBounds(30, 30, 550, 600);
		exe = new Button(executeGroup, SWT.PUSH);
		exe.setText("Enter");
		exe.setBounds(700, 30, 50, 30);
		exe.addSelectionListener(new SelectionAdapter() {
			public void widgetSelected(SelectionEvent event) {
				String str;
				try {
					str = "python C:\\scheme-kr-interpreter\\mycode.py --codes \"" + t1.getText() + "\"";
					str = str.replace("\n", "-*-*-");
//					System.out.println(str);
					ps = Runtime.getRuntime().exec(str);
					br = new BufferedReader(new InputStreamReader(ps.getInputStream(), "euc-kr"));
					System.out.println(br.readLine().replace("-*-*-", "\n"));
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		});
	}
}